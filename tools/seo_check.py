#!/usr/bin/env python3
"""Static SEO checks for the built site. Standard library only (uses macOS `sips` for image sizes when available).

Usage:  python3 tools/seo_check.py [site_dir] [--json out.json]
Exit code is 1 when a blocking problem is found (broken link, invalid JSON-LD, missing title, etc).
"""
import itertools, json, os, re, shutil, subprocess, sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

args = [a for a in sys.argv[1:]]
JSON_OUT = None
if "--json" in args:
    i = args.index("--json"); JSON_OUT = args[i + 1]; del args[i:i + 2]
ROOT = args[0] if args else "."


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self.metas = {}; self.canon = []; self.heads = []; self.links = []; self.imgs = []
        self.ld = []; self.ids = []; self.forms = []; self.inputs = []; self.labels = []; self.text = []
        self.preloads = []; self.scripts = []
        self._h = None; self._t = False; self._ld = None; self._skip = 0; self._a = None; self._main = 0

    def handle_starttag(self, t, a):
        a = dict(a)
        if a.get("id"): self.ids.append(a["id"])
        if t == "title": self._t = True
        elif t == "meta":
            k = a.get("name") or a.get("property")
            if k: self.metas[k] = a.get("content", "")
        elif t == "link":
            if a.get("rel") == "canonical": self.canon.append(a.get("href"))
            if a.get("rel") == "preload": self.preloads.append(a.get("href"))
        elif t in ("h1", "h2", "h3", "h4", "h5", "h6"): self._h = [t, ""]
        elif t == "a":
            self._a = dict(href=a.get("href") or "", text="", main=self._main > 0, hidden=a.get("tabindex") == "-1")
            self.links.append(self._a)
        elif t == "img": self.imgs.append(a)
        elif t == "script":
            if a.get("type") == "application/ld+json": self._ld = ""
            else:
                self.scripts.append(a.get("src") or "inline"); self._skip += 1
        elif t in ("style", "svg", "select"): self._skip += 1
        elif t == "form": self.forms.append(a)
        elif t in ("input", "textarea"): self.inputs.append(a)
        elif t == "label": self.labels.append(a.get("for"))
        elif t == "main": self._main += 1
        if t == "select": self.inputs.append(a)

    def handle_endtag(self, t):
        if t == "title": self._t = False
        elif t in ("h1", "h2", "h3", "h4", "h5", "h6") and self._h:
            self.heads.append((self._h[0], re.sub(r"\s+", " ", self._h[1]).strip())); self._h = None
        elif t == "a": self._a = None
        elif t == "script":
            if self._ld is not None: self.ld.append(self._ld); self._ld = None
            else: self._skip = max(0, self._skip - 1)
        elif t in ("style", "svg", "select"): self._skip = max(0, self._skip - 1)
        elif t == "main": self._main -= 1

    def handle_data(self, x):
        if self._t: self.title += x
        if self._ld is not None: self._ld += x; return
        if self._h is not None: self._h[1] += x
        if self._a is not None: self._a["text"] += x
        if self._main > 0 and not self._skip: self.text.append(x)


# Google Search Console verification files (googleXXXX.html) are not site pages.
files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html") and not re.fullmatch(r"google[0-9a-f]+\.html", f))
pages = {}
for f in files:
    p = Page(); p.feed(open(os.path.join(ROOT, f), encoding="utf-8").read()); pages[f] = p

images = {}
img_dir = os.path.join(ROOT, "images")
for f in sorted(os.listdir(img_dir)) if os.path.isdir(img_dir) else []:
    fp = os.path.join(img_dir, f); w = h = None
    if shutil.which("sips"):
        o = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", fp], capture_output=True, text=True).stdout
        m1, m2 = re.search(r"pixelWidth: (\d+)", o), re.search(r"pixelHeight: (\d+)", o)
        w, h = int(m1[1]) if m1 else None, int(m2[1]) if m2 else None
    images[f] = dict(w=w, h=h, kb=round(os.path.getsize(fp) / 1024))

NOINDEX = {f for f, p in pages.items() if "noindex" in p.metas.get("robots", "")}
errors, warnings = [], []
inbound, inbound_body = Counter(), Counter()
anchors = defaultdict(Counter)
external = Counter()
rows = {}

for f, p in pages.items():
    body = re.sub(r"\s+", " ", " ".join(p.text)).strip()
    h1 = [x for t, x in p.heads if t == "h1"]
    if not p.title.strip(): errors.append(f"{f}: missing title")
    if not p.metas.get("description"): errors.append(f"{f}: missing meta description")
    if len(h1) != 1: errors.append(f"{f}: {len(h1)} h1 tags")
    if f not in NOINDEX and f != "404.html":
        if len(p.canon) != 1: errors.append(f"{f}: {len(p.canon)} canonical tags")
        else:
            want = "https://htbelectrical.com.au/" + ("" if f == "index.html" else f)
            if p.canon[0] != want: errors.append(f"{f}: canonical {p.canon[0]} != {want}")
    for raw in p.ld:
        try: json.loads(raw)
        except Exception as e: errors.append(f"{f}: invalid JSON-LD ({e})")
    for k, v in Counter(p.ids).items():
        if v > 1: errors.append(f"{f}: duplicate id {k}")
    prev = 0
    skips = []
    for t, x in p.heads:
        n = int(t[1])
        if prev and n > prev + 1: skips.append(f"h{prev}>h{n} '{x[:40]}'")
        prev = n
    if skips: warnings.append(f"{f}: heading skip {skips}")
    for l in p.links:
        u = urlparse(l["href"])
        if u.scheme in ("tel", "mailto"): continue
        if u.scheme in ("http", "https"): external[l["href"]] += 1; continue
        path = unquote(u.path).lstrip("/")
        if u.path == "/" or (not path and not u.fragment and l["href"] != ""): path = "index.html"
        if not path:
            if u.fragment and u.fragment not in p.ids: errors.append(f"{f}: missing anchor #{u.fragment}")
            continue
        if not os.path.exists(os.path.join(ROOT, path)): errors.append(f"{f}: broken link {l['href']}"); continue
        if u.fragment and path in pages and u.fragment not in pages[path].ids: errors.append(f"{f}: missing anchor {l['href']}")
        if path != f:
            inbound[path] += 1
            if l["main"]: inbound_body[path] += 1
            anchors[path][re.sub(r"\s+", " ", l["text"]).strip()] += 1
    for im in p.imgs:
        n = os.path.basename(im.get("src", ""))
        if n not in images: errors.append(f"{f}: missing image {n}"); continue
        if not im.get("alt"): errors.append(f"{f}: image without alt {n}")
        r = images[n]
        if not (im.get("width") and im.get("height")): warnings.append(f"{f}: image without dimensions {n}")
        elif r["w"] and abs(int(im["width"]) / int(im["height"]) - r["w"] / r["h"]) / (r["w"] / r["h"]) > 0.03:
            warnings.append(f"{n}: width/height attrs {im['width']}x{im['height']} but file is {r['w']}x{r['h']}")
    labelled = set(p.labels)
    for i in p.inputs:
        if i.get("type") in ("hidden", "submit"): continue
        if i.get("id") not in labelled and not i.get("aria-label") and i.get("aria-hidden") != "true":
            warnings.append(f"{f}: unlabelled field {i.get('name')}")
    tel = [l for l in p.links if l["href"].startswith("tel:") and not l["hidden"]]
    types = []
    for raw in p.ld:
        try:
            j = json.loads(raw)
            for n in (j.get("@graph") or [j]): types.append(n.get("@type"))
        except Exception: pass
    rows[f] = dict(title=p.title, title_len=len(p.title), desc=p.metas.get("description", ""), desc_len=len(p.metas.get("description", "")),
                   robots=p.metas.get("robots", ""), canonical=p.canon[0] if p.canon else "", h1=h1[0] if h1 else "",
                   h2=[x for t, x in p.heads if t == "h2"], words=len(body.split()), tel_links=len(tel), forms=len(p.forms),
                   schema=types, images=len(p.imgs), scripts=p.scripts, _text=body)

indexable = [f for f in files if f not in NOINDEX and f != "404.html"]
for f in indexable:
    if rows[f]["title_len"] > 65: warnings.append(f"{f}: title {rows[f]['title_len']} chars")
    if rows[f]["desc_len"] > 165: warnings.append(f"{f}: description {rows[f]['desc_len']} chars")
    if rows[f]["desc_len"] < 110: warnings.append(f"{f}: description {rows[f]['desc_len']} chars")
    if not inbound_body[f] and f != "index.html": warnings.append(f"{f}: no in-content inbound links")
for k, v in Counter(rows[f]["title"] for f in indexable).items():
    if v > 1: errors.append(f"duplicate title x{v}: {k}")
for k, v in Counter(rows[f]["desc"] for f in indexable).items():
    if v > 1: errors.append(f"duplicate description x{v}: {k}")

sm = os.path.join(ROOT, "sitemap.xml")
if os.path.exists(sm):
    locs = re.findall(r"<loc>([^<]+)</loc>", open(sm, encoding="utf-8").read())
    want = {"https://htbelectrical.com.au/" + ("" if f == "index.html" else f) for f in indexable}
    for x in sorted(set(locs) - want): errors.append(f"sitemap lists non-indexable URL {x}")
    for x in sorted(want - set(locs)): errors.append(f"sitemap is missing {x}")
else:
    errors.append("sitemap.xml missing")


def shingles(t):
    w = re.findall(r"[a-z0-9']+", t.lower())
    return {" ".join(w[i:i + 5]) for i in range(max(0, len(w) - 4))}


sh = {f: shingles(rows[f]["_text"]) for f in files}
def jac(a, b): return len(sh[a] & sh[b]) / max(1, len(sh[a] | sh[b]))
def stats(group):
    v = [jac(a, b) for a, b in itertools.combinations(group, 2)]
    return dict(pairs=len(v), mean=round(sum(v) / len(v), 3), min=round(min(v), 3), max=round(max(v), 3)) if v else {}
suburbs = [f for f in files if f.startswith("electrician-")]
unique = {}
for f in suburbs:
    others = set().union(*(sh[o] for o in suburbs if o != f))
    unique[f] = round(len(sh[f] - others) / max(1, len(sh[f])), 3)
for r in rows.values(): r.pop("_text")

report = dict(pages=rows, inbound=dict(inbound), inbound_body=dict(inbound_body), images=images, external=dict(external),
              anchors={k: dict(v.most_common(5)) for k, v in anchors.items()},
              similarity=dict(suburb_pages=stats(suburbs), suburb_unique_share=unique), errors=errors, warnings=warnings)
if JSON_OUT: json.dump(report, open(JSON_OUT, "w"), indent=1, ensure_ascii=False)

print(f"{'page':50}{'title':>6}{'desc':>6}{'words':>7}{'tel':>5}{'in':>5}{'body':>6}")
for f, r in rows.items():
    print(f"{f:50}{r['title_len']:>6}{r['desc_len']:>6}{r['words']:>7}{r['tel_links']:>5}{inbound[f]:>5}{inbound_body[f]:>6}")
print("\nSuburb page similarity:", report["similarity"]["suburb_pages"])
print("Suburb unique text share: min", min(unique.values()), "max", max(unique.values()))
print("Images:", len(images), "files,", sum(v["kb"] for v in images.values()), "KB total")
print(f"\nWARNINGS ({len(warnings)})")
for k, v in Counter(warnings).most_common(): print(" -", k, f"(x{v})" if v > 1 else "")
print(f"\nERRORS ({len(errors)})")
for e in errors: print(" -", e)
sys.exit(1 if errors else 0)
