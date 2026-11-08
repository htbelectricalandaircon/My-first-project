import html, os, sys
from urllib.parse import quote

OUT = sys.argv[1]
PHONE = "0403 116 368"
TEL = "tel:+61403116368"
EMAIL = "info@htbelectrical.com.au"
LICENCE = "376869C"
SITE = "https://htbelectricalandaircon.github.io/my-first-project"
GOOGLE_PROFILE = "https://www.google.com/maps/search/?api=1&amp;query=HTB%20ELECTRICAL%20%26%20AIR%20CONDITIONING%20P%2FL"
GOOGLE_REVIEW = "https://g.page/htbelectrical/review?rc"
FORM_ACTION = "https://formsubmit.co/" + EMAIL
TODO = lambda s: f'<span class="todo">{s}</span>'

ICONS = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-phone" viewBox="0 0 24 24"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></symbol>
  <symbol id="i-mail" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></symbol>
  <symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></symbol>
  <symbol id="i-bolt" viewBox="0 0 24 24"><path d="M13 2 3 14h9l-1 8 10-12h-9z"/></symbol>
  <symbol id="i-star" viewBox="0 0 24 24"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></symbol>
  <symbol id="i-menu" viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"/></symbol>
  <symbol id="i-user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1"/></symbol>
  <symbol id="i-home" viewBox="0 0 24 24"><path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></symbol>
  <symbol id="i-wrench" viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></symbol>
  <symbol id="i-board" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6v5M12 6v5M16 6v5M8 15h8M8 18h8"/></symbol>
  <symbol id="i-aircon" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="9" rx="2"/><path d="M6 9.5h12M7 16.5c0 1.5 1 2 1 3.5M12 16v4M17 16.5c0 1.5-1 2-1 3.5"/></symbol>
  <symbol id="i-snow" viewBox="0 0 24 24"><path d="M12 2v20M4.9 7l14.2 10M4.9 17 19.1 7M9 4l3 3 3-3M9 20l3-3 3 3"/></symbol>
  <symbol id="i-ev" viewBox="0 0 24 24"><path d="M4 21V5a2 2 0 0 1 2-2h7a2 2 0 0 1 2 2v16M2 21h15M15 9h2a2 2 0 0 1 2 2v4a1.5 1.5 0 0 0 3 0V8l-3-3"/><path d="m10.5 7-2.5 4.5h3L8.5 16"/></symbol>
  <symbol id="i-outlet" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8.5 8.5 10 11M15.5 8.5 14 11M12 14v3"/></symbol>
  <symbol id="i-bulb" viewBox="0 0 24 24"><path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.2 1 2v.3h6v-.3c0-.8.4-1.5 1-2A7 7 0 0 0 12 2z"/></symbol>
  <symbol id="i-fan" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="1.5"/><path d="M12 10.5C12 7.5 13 5 15 5s2 3-1.5 5.5M13.5 12c3 0 5.5 1 5.5 3s-3 2-5.5-1.5M12 13.5c0 3-1 5.5-3 5.5s-2-3 1.5-5.5M10.5 12C7.5 12 5 11 5 9s3-2 5.5 1.5"/></symbol>
  <symbol id="i-ceilingfan" viewBox="0 0 24 24"><path d="M12 2v6M12 8a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM10 10H3l1.5 2H10M14 10h7l-1.5 2H14M12 12v4"/><circle cx="12" cy="18" r="2"/></symbol>
  <symbol id="i-network" viewBox="0 0 24 24"><rect x="9" y="2" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="16" y="16" width="6" height="6" rx="1"/><path d="M12 8v4M5 16v-4h14v4"/></symbol>
  <symbol id="i-tv" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/></symbol>
  <symbol id="i-antenna" viewBox="0 0 24 24"><circle cx="12" cy="9" r="2"/><path d="M12 11v11M8 22h8M8.2 5.2a5.5 5.5 0 0 0 0 7.6M15.8 5.2a5.5 5.5 0 0 1 0 7.6M5.3 2.3a9.5 9.5 0 0 0 0 13.4M18.7 2.3a9.5 9.5 0 0 1 0 13.4"/></symbol>
  <symbol id="i-swap" viewBox="0 0 24 24"><path d="M17 3l4 4-4 4M3 7h18M7 21l-4-4 4-4M21 17H3"/></symbol>
  <symbol id="i-plug" viewBox="0 0 24 24"><path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 0 1-12 0zM12 18v4"/></symbol>
  <symbol id="i-downlight" viewBox="0 0 24 24"><path d="M3 5h18M7 5a5 5 0 0 0 10 0M12 14v2M7.5 13l-1.5 2M16.5 13l1.5 2M12 19v2M5 19l-1.5 1.5M19 19l1.5 1.5"/></symbol>
  <symbol id="i-pendant" viewBox="0 0 24 24"><path d="M12 2v6M8 8h8l3 7H5zM10 18a2 2 0 0 0 4 0"/></symbol>
  <symbol id="i-smoke" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M12 3v2M12 19v2"/></symbol>
  <symbol id="i-cooktop" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="18" rx="2"/><circle cx="8" cy="8" r="2"/><circle cx="16" cy="8" r="2"/><path d="M2 13h20M7 17h10"/></symbol>
  <symbol id="i-doorbell" viewBox="0 0 24 24"><rect x="6" y="2" width="12" height="20" rx="3"/><circle cx="12" cy="8" r="2"/><circle cx="12" cy="16" r="2.5"/></symbol>
  <symbol id="i-camera" viewBox="0 0 24 24"><path d="M3 7h13l5 3-2 4H3z"/><circle cx="16" cy="10.5" r="1.2"/><path d="M7 14v4H3M7 18h4"/></symbol>
  <symbol id="i-duct" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="8" rx="1"/><path d="M6 8h12M7 15l-1 4M12 15v4M17 15l1 4"/></symbol>
  <symbol id="i-towelrail" viewBox="0 0 24 24"><path d="M6 3v18M18 3v18M6 7h12M6 11h12M6 15h12M6 19h12"/></symbol>
  <symbol id="i-family" viewBox="0 0 24 24"><circle cx="8" cy="7" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M2 21v-1a6 6 0 0 1 12 0v1M14 21v-.5a4 4 0 0 1 8 0v.5"/></symbol>
</svg>"""

def ico(name, cls="ico"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'

NAV = [("index.html", "Home"), ("services.html", "Services"), ("about.html", "About"),
       ("locations.html", "Locations"), ("contact.html", "Contact")]

SERVICE_OPTIONS = [
    ("Electrical", ["Electrical repairs & fault finding", "Switchboard upgrade", "Ceiling fan installation", "Downlight installation", "Pendant light installation", "Smoke alarm installation", "Cooktop & oven installation", "Smart doorbell installation", "Security camera installation",
                    "Power point installation", "LED strip lighting", "Exhaust fan installation", "Heated towel rail installation",
                    "EV charger installation", "Network cabling", "TV wall mounting", "TV antenna"]),
    ("Air conditioning", ["Split system air conditioning installation", "Ducted air conditioning installation", "Air conditioner replacement",
                          "Air conditioning service & maintenance", "Air conditioning repairs"]),
]

def page(filename, title, description, body, active=None):
    links = "\n".join(
        f'        <li><a href="{href}"{" class=\"active\"" if href == active else ""}>{label}</a></li>'
        for href, label in NAV)
    return f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="icon" type="image/png" href="images/icon.png">
  <link rel="apple-touch-icon" href="images/icon.png">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
{ICONS}

  <div class="topbar">
    <div class="container">
      <span>{ico("clock")}<strong>Open 24 hours, 7 days</strong></span>
      <div class="tb-right">
        <a class="tb-mail" href="mailto:{EMAIL}">{ico("mail")}{EMAIL}</a>
        <a href="{TEL}">{ico("phone")}<strong>{PHONE}</strong></a>
      </div>
    </div>
  </div>

  <header>
    <div class="container nav">
      <a href="index.html" class="brand"><img src="images/logo.png" alt="HTB Electrical &amp; Air Conditioning Pty Ltd" width="600" height="305"></a>
      <button class="menu-btn" id="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="nav-links">{ico("menu")}</button>
      <ul class="nav-links" id="nav-links">
{links}
        <li><a href="quote.html" class="btn btn-red btn-sm">Get a Quote</a></li>
      </ul>
    </div>
  </header>

  <main>
{body}
  </main>

  <footer>
    <div class="container">
      <div class="foot-grid">
        <div>
          <h3>HTB Electrical &amp; Air Conditioning Pty Ltd</h3>
          <p class="tag">North Sydney Electrical &amp; Air Conditioning Technicians</p>
          <ul style="margin-top:14px">
            <li>ABN: 54 168 092 466</li>
            <li>Electrical Licence No: {LICENCE}</li>
          </ul>
        </div>
        <div>
          <h3>Quick Links</h3>
          <ul>
            <li><a href="services.html">Our Services</a></li>
            <li><a href="about.html">About Us</a></li>
            <li><a href="locations.html">Areas We Service</a></li>
            <li><a href="quote.html">Get a Quote or Booking</a></li>
            <li><a href="{GOOGLE_REVIEW}" target="_blank" rel="noopener">Review us on Google</a></li>
          </ul>
        </div>
        <div>
          <h3>Contact</h3>
          <ul>
            <li><a class="line" href="{TEL}">{ico("phone")}{PHONE}</a></li>
            <li><a class="line" href="mailto:{EMAIL}">{ico("mail")}{EMAIL}</a></li>
            <li class="line">{ico("clock")}Open 24 hours, 7 days</li>
            <li class="line">{ico("pin")}North Sydney NSW</li>
          </ul>
        </div>
      </div>
      <div class="foot-bottom">&copy; <span id="year">2026</span> HTB Electrical &amp; Air Conditioning Pty Ltd. All rights reserved.</div>
    </div>
  </footer>

  <a href="{TEL}" class="btn btn-red call-float" id="call-float">{ico("phone")}Call Now – {PHONE}</a>

  <script src="site.js"></script>
</body>
</html>
"""

def service_select(required=True):
    groups = "".join(
        f'<optgroup label="{g}">' + "".join(f"<option>{html.escape(o)}</option>" for o in opts) + "</optgroup>"
        for g, opts in SERVICE_OPTIONS)
    return f"""<select id="{{p}}-service" name="service"{" required" if required else ""}>
                  <option value="">Select a service…</option>
                  {groups}
                  <option>Other</option>
                </select>"""

def hidden_fields(subject):
    return f"""<input type="hidden" name="_subject" value="{subject}">
            <input type="hidden" name="_next" value="{SITE}/thanks.html">
            <input type="hidden" name="_template" value="table">
            <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">"""

def short_form(p, heading, hint, subject, card_cls="form-card"):
    return f"""<form class="{card_cls}" action="{FORM_ACTION}" method="POST" enctype="multipart/form-data">
            {hidden_fields(subject)}
            <h2>{heading}</h2>
            <p class="hint">{hint}</p>
            <div class="field">
              <label for="{p}-name">Full name</label>
              <input id="{p}-name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="form-row">
              <div class="field">
                <label for="{p}-phone">Phone</label>
                <input id="{p}-phone" name="phone" type="tel" autocomplete="tel" required>
              </div>
              <div class="field">
                <label for="{p}-email">Email</label>
                <input id="{p}-email" name="email" type="email" autocomplete="email" required>
              </div>
            </div>
            <div class="field">
              <label for="{p}-address">Address</label>
              <input id="{p}-address" name="address" type="text" autocomplete="street-address" required>
            </div>
            <div class="field">
              <label for="{p}-service">Service needed</label>
              {service_select().replace("{p}", p)}
            </div>
            <div class="field">
              <label for="{p}-message">How can we help?</label>
              <textarea id="{p}-message" name="message" placeholder="Briefly describe the work you need…" style="min-height:80px"></textarea>
            </div>
            <div class="field">
              <label for="{p}-file">Attachment <span class="opt">(optional)</span></label>
              <input id="{p}-file" name="attachment" type="file" accept="image/*,.pdf">
              <p class="help">Attach a photo or document of the job (max 5 MB).</p>
            </div>
            <button type="submit" class="btn btn-red btn-block">Submit</button>
          </form>"""

def page_hero(title, sub, extra="", photo=None):
    style = f' style="--photo:url(images/{photo})"' if photo else ""
    cls = "page-hero has-photo" if photo else "page-hero"
    return f"""    <section class="{cls}"{style}>
      <div class="container">
        <h1>{title}</h1>
        <p>{sub}</p>{extra}
      </div>
    </section>"""

CTA = f"""    <div class="cta">
      <div class="container">
        <h2>Need an electrician or air conditioning technician?</h2>
        <p>We're available 24 hours a day, 7 days a week.</p>
        <div class="actions">
          <a href="{TEL}" class="btn btn-white">{ico("phone")}Call {PHONE}</a>
          <a href="quote.html" class="btn btn-outline">Get a Free Quote</a>
        </div>
      </div>
    </div>"""

# ---------- Services data ----------
SERVICES = [
    ("electrical", "bolt", "Electrical Services",
     "Safe, reliable electrical work for homes and businesses – from small repairs to new installations.",
     [("wrench", "Electrical Repairs & Fault Finding", "Electrical repairs & fault finding",
       "Power outages, tripping safety switches, faulty wiring, flickering lights – we find the fault and fix it safely."),
      ("board", "Switchboard Upgrades", "Switchboard upgrade",
       "Replace old fuse boards with modern switchboards, circuit breakers and safety switches to protect your family."),
      ("ceilingfan", "Ceiling Fan Installation", "Ceiling fan installation",
       "Supply and installation of ceiling fans and ceiling lights, including new wiring and wall controls."),
      ("downlight", "Downlight Installation", "Downlight installation",
       "New LED downlights and replacement of old halogen downlights with energy-efficient LEDs."),
      ("pendant", "Pendant Light Installation", "Pendant light installation",
       "Installation of pendant lights over kitchen benches, dining tables and entryways."),
      ("smoke", "Smoke Alarm Installation", "Smoke alarm installation",
       "Installation and replacement of smoke alarms to keep your home safe and compliant."),
      ("cooktop", "Cooktop & Oven Installation", "Cooktop & oven installation",
       "Electrical connection and installation of cooktops and ovens, including new circuits if required."),
      ("doorbell", "Smart Doorbell Installation", "Smart doorbell installation",
       "Installation of smart video doorbells, so you can see and talk to visitors from your phone."),
      ("camera", "Security Camera Installation", "Security camera installation",
       "Installation of security cameras to help protect your home or business."),
      ("outlet", "Power Point Installation", "Power point installation",
       "New and additional power points, USB outlets, outdoor power points and relocations."),
      ("bulb", "LED Strip Lighting", "LED strip lighting",
       "Feature and under-cabinet LED strip lighting for kitchens, living areas, stairs and shops."),
      ("fan", "Exhaust Fans", "Exhaust fan installation",
       "Bathroom, kitchen and laundry exhaust fans – new installations and replacements."),
      ("towelrail", "Heated Towel Rail Installation", "Heated towel rail installation",
       "Supply and installation of heated towel rails, including the wiring and switch, for warm, dry towels every day."),
      ("ev", "EV Charger Installation", "EV charger installation",
       "Home and business electric vehicle charger installation, including any wiring or switchboard work needed."),
      ("network", "Network Cabling", "Network cabling",
       "Data points and network cabling for reliable internet in homes and offices."),
      ("tv", "TV Wall Mounting", "TV wall mounting",
       "Secure TV wall mounting with neat, concealed cabling and power points behind the TV."),
      ("antenna", "TV Antennas", "TV antenna",
       "TV antenna installation, repairs and extra TV points.")]),
    ("ac-installation", "aircon", "Air Conditioning Installation",
     "Stay cool in summer and warm in winter with a professionally installed split system or ducted system.",
     [("aircon", "Split System Installation", "Split system air conditioning installation",
       "Supply and installation of split system air conditioners for bedrooms, living areas and offices."),
      ("duct", "Ducted Air Conditioning Installation", "Ducted air conditioning installation",
       "Supply and installation of ducted air conditioning systems for whole-home comfort, with discreet vents in every room."),
      ("swap", "Air Conditioner Replacement", "Air conditioner replacement",
       "Remove your old or broken unit and install a new, energy-efficient system."),
      ("plug", "Dedicated Power Circuits", "Split system air conditioning installation",
       "As licensed electricians, we also install the power circuit for your new air conditioner – no need for a separate electrician.")]),
    ("ac-service", "snow", "Air Conditioning Service, Maintenance & Repairs",
     "Keep your air conditioner running efficiently and fix problems fast.",
     [("snow", "Servicing & Maintenance", "Air conditioning service & maintenance",
       "Cleaning of filters and coils and a full check of your system, so it runs efficiently and lasts longer."),
      ("wrench", "Air Conditioning Repairs", "Air conditioning repairs",
       "Not cooling or heating, leaking water, strange noises or error codes – we diagnose and repair the problem.")]),
]

# ---------- Locations data ----------
REGIONS = [
    ("Sydney CBD", ["Sydney", "The Rocks", "Barangaroo", "Millers Point", "Dawes Point", "Haymarket"]),
    ("Lower North Shore", ["Chatswood", "Waverton", "Roseville", "Northbridge", "North Sydney", "Neutral Bay",
                           "Naremburn", "Milsons Point", "Middle Cove", "McMahons Point"]),
    ("Northern Beaches", ["North Manly", "North Balgowlah", "Queenscliff", "Freshwater", "Elanora Heights",
                          "Clontarf"]),
    ("Ryde District", ["North Ryde", "Melrose Park", "Marsfield", "Putney", "Tennyson Point", "Gladesville",
                       "Eastwood", "East Ryde", "Ryde"]),
    ("Inner West", ["Marrickville", "Lilyfield", "Haberfield", "Summer Hill", "Sydenham", "Tempe"]),
    ("Hills District", ["North Epping", "Box Hill", "Winston Hills",
                        "Norwest", "Kenthurst", "Bella Vista"]),
    ("Eastern Suburbs", ["Woollahra", "Watsons Bay", "Vaucluse", "Surry Hills", "South Coogee", "Rushcutters Bay",
                         "Queens Park", "Port Botany", "Potts Point", "Phillip Bay"]),
]

# ---------- Recent work gallery ----------
WORK = [
    ("work-split-system.jpg", "Split system air conditioning installation"),
    ("work-switchboard.jpg", "Switchboard upgrade with RCD safety switches"),
    ("work-ev-charger.jpg", "Tesla EV charger installation"),
    ("work-pendants.jpg", "Pendant light installation"),
    ("work-downlights.jpg", "LED downlight installation"),
    ("work-led-stairs.jpg", "LED strip lighting on staircase"),
    ("work-cooktop.jpg", "Cooktop installation"),
    ("work-tv-mount.jpg", "TV wall mounting"),
    ("work-antenna.jpg", "TV antenna installation"),
    ("work-led-mirror.jpg", "Backlit LED mirror installation"),
    ("work-chandelier.jpg", "Feature light installation"),
    ("work-led-robe.jpg", "LED strip lighting in walk-in robe"),
    ("work-towel-rail.jpg", "Heated towel rail installation"),
    ("work-commercial.jpg", "Commercial kitchen electrical work"),
]
def gallery(items):
    return "".join(f"""
          <figure class="work">
            <img src="images/{f}" alt="{c}" loading="lazy" width="800" height="1067">
            <figcaption>{c}</figcaption>
          </figure>""" for f, c in items)

# ---------- Home ----------
cat_cards = ""
for sid, icon, title, intro, items in SERVICES:
    ticks = "".join(f"<li>{ico('check')}{t}</li>" for _, t, _, _ in items[:5])
    if len(items) > 5:
        ticks += f"<li>{ico('check')}…and more</li>"
    cat_cards += f"""
          <div class="cat-card">
            <img class="cat-img" src="images/svc-{sid}.jpg" alt="{title}" loading="lazy" width="900" height="600">
            <div class="icon-wrap">{ico(icon)}</div>
            <h3>{title}</h3>
            <p>{intro}</p>
            <ul class="tick-list">{ticks}</ul>
            <a class="more" href="services.html#{sid}">View services →</a>
          </div>"""

stars = "".join(ico("star", "ico ico-fill") for _ in range(5))
REVIEWS = [
    ("Kobie W.", "Split system installation", [
        "Excellent service from start to finish.",
        "I can't recommend Tony highly enough. From our very first contact, his communication was open, clear, and honest. He offered a free consultation and quote, and his pricing was very reasonable, with no surprises or pressure.",
        "Tony was incredibly responsive, always quick to reply to calls and messages and answering my questions and providing extra details required for strata approval promptly. On installation day, he was efficient, professional, and clean respectful in my home. You'd hardly know anyone had been working there.",
        "The split system is running great and I couldn't be happier. If you're looking for a reliable, fair-priced installer who genuinely cares about doing the job well, call Tony. I'll definitely be using him again for any future work."]),
    ("Dru C.", "Ducted heating repair", [
        "Recently had Tony out to fix ducted heating that had stopped working. Tony was communicative about his eta and very friendly too. He managed to fix the heating and also explained what had happened and also walked me through how to get the best out of the system. I've been scammed and over charged before with another sparky, but Tony was honest and fairly priced. As a single woman it's nice to have a local tradesman I can trust. I have no hesitation recommending Tony for any electrical work. Trustworthy Tony!"]),
    ("Elizabeth F.", "Electrical work", [
        "Tony is an amazing electrician who has done a lot of jobs for us over the years. He is responsive, prompt, reliable and does a great job. He always leaves the site neat and clean and goes above and beyond. I highly recommend this service."]),
]
review_cards = "".join(f"""
          <div class="review">
            <div class="stars">{stars}</div>
            <blockquote>{"".join(f"<p>{html.escape(para)}</p>" for para in paras)}</blockquote>
            <div class="who">{name}</div>
            <div class="where">{job} · Google review</div>
          </div>""" for name, job, paras in REVIEWS)

home = f"""    <section class="hero">
      <div class="container hero-grid">
        <div>
          <span class="eyebrow"><span class="dot"></span>OPEN 24 HOURS · 7 DAYS</span>
          <h1>North Sydney Electrical &amp; Air Conditioning Specialists</h1>
          <p class="lead">Family-owned electricians and air conditioning technicians, servicing homes and businesses across Sydney.</p>
          <ul class="usp-list">
            <li><span class="usp-ico">{ico("bolt")}</span>Fast, local &amp; reliable</li>
            <li><span class="usp-ico stars">{ico("star", "ico ico-fill")}</span><a href="{GOOGLE_PROFILE}" target="_blank" rel="noopener" class="usp-link">5.0-star Google rating – 347 reviews</a></li>
            <li><span class="usp-ico">{ico("shield")}</span>Fully licensed &amp; insured</li>
          </ul>
          <div class="hero-actions">
            <a href="{TEL}" class="btn btn-red">{ico("phone")}Call {PHONE}</a>
            <a href="services.html" class="btn btn-outline">Our Services</a>
          </div>
        </div>
        <div id="quote">
          {short_form("h", "Get a Free Quote or Booking", "Fill in your details and we'll be in contact as soon as we can.", "New quote request – website (home page)")}
        </div>
      </div>
    </section>

    <div class="strip">
      <div class="container strip-inner">
        <span class="strip-label">Proudly servicing Sydney with:</span>
        <span class="strip-item">{ico("bolt")}Electrical Service &amp; Repairs</span>
        <span class="strip-item">{ico("aircon")}Split &amp; Ducted Air Conditioning Installation</span>
      </div>
    </div>

    <section class="welcome">
      <div class="container welcome-grid">
      <div class="welcome-inner">
        <h2 class="section-title">A Family Business You Can Trust</h2>
        <p class="welcome-lead">Welcome to HTB Electrical &amp; Air Conditioning, a family-owned North Sydney business with more than 10 years of experience looking after homes across Sydney.</p>
        <p>We treat every customer like family, and you always come first. Every job, big or small, gets the same care and attention we’d give our own family’s home. Whether you need a quick electrical repair, a new installation, or air conditioning to keep you comfortable all year round, our friendly team will turn up on time, explain things in plain English, and get the job done right the first time.</p>
        <p>Our work is reliable, professional, and always completed to meet safety requirements and Australian Standards. And we have one golden rule: we leave your place clean and tidy, just like we were never there. No mess, no dust, no leftover offcuts, just great work you’ll be happy with.</p>
        <p>As a family business, our name is on every job, and we take that seriously. Many of our customers have been with us for years, and we’d love to look after you too.</p>
        <p class="welcome-close">Give us a call today and see the difference a family business makes.</p>
        <div class="hero-actions">
          <a href="{TEL}" class="btn btn-red">{ico("phone")}Call {PHONE}</a>
          <a href="quote.html" class="btn btn-navy-outline">Get a Free Quote</a>
        </div>
      </div>
      <img class="welcome-img" src="images/welcome-tony.jpg" alt="Tony Bui with the HTB Electrical &amp; Air Conditioning van near the Sydney Harbour Bridge" loading="lazy" width="1400" height="966">
      </div>
    </section>

    <section class="bg-soft">
      <div class="container">
        <div class="center">
          <h2 class="section-title">Our Services</h2>
          <p class="section-intro">One call covers your electrical work and your air conditioning – installation, servicing and repairs.</p>
        </div>
        <div class="cat-grid">{cat_cards}
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="center">
          <h2 class="section-title">Our Recent Work</h2>
          <p class="section-intro">Real jobs completed by Tony for homes and businesses across Sydney.</p>
        </div>
        <div class="work-grid">{gallery(WORK[:8])}
        </div>
        <div class="center" style="margin-top:28px">
          <a href="services.html#work" class="btn btn-navy-outline">See more of our work</a>
        </div>
      </div>
    </section>

    <section class="bg-soft">
      <div class="container">
        <div class="center">
          <h2 class="section-title">What Our Clients Say</h2>
          <div class="rating-badge">
            <span class="rating-num">5.0</span>
            <span class="stars">{stars}</span>
            <span>from <strong>347 Google reviews</strong></span>
          </div>
        </div>
        <div class="review-grid">{review_cards}
        </div>
        <div class="hero-actions" style="justify-content:center;margin-top:28px">
          <a href="{GOOGLE_PROFILE}" class="btn btn-red" target="_blank" rel="noopener">{ico("star", "ico ico-fill")}Read our Google reviews</a>
          <a href="{GOOGLE_REVIEW}" class="btn btn-navy-outline" target="_blank" rel="noopener">{ico("star", "ico ico-fill")}Review us on Google</a>
        </div>
      </div>
    </section>

    <section class="bg-soft">
      <div class="container center">
        <h2 class="section-title">Areas We Service</h2>
        <p class="section-intro">Based in North Sydney, we work Sydney wide, including:</p>
        <ul class="chips" style="justify-content:center;margin-bottom:24px">
          {"".join(f"<li>{r}</li>" for r, _ in REGIONS)}
        </ul>
        <a href="locations.html" class="btn btn-navy-outline">See all suburbs</a>
      </div>
    </section>

{CTA}"""

# ---------- Services ----------
svc_sections = ""
for i, (sid, icon, title, intro, items) in enumerate(SERVICES):
    cards = "".join(f"""
            <div class="svc-item">
              <h3>{ico(ic)}{t}</h3>
              <p>{d}</p>
              <a class="btn btn-red btn-sm" href="quote.html?service={quote(opt)}">Get a quote</a>
            </div>""" for ic, t, opt, d in items)
    svc_sections += f"""
    <section id="{sid}"{' class="bg-soft"' if i % 2 == 0 else ""}>
      <div class="container">
        <div class="svc-head">
          <div class="icon-wrap">{ico(icon)}</div>
          <h2 class="section-title">{title}</h2>
        </div>
        <p class="section-intro">{intro}</p>
        <img class="svc-banner" src="images/banner-{sid}.jpg" alt="{title}" loading="lazy" width="1400" height="500">
        <div class="svc-grid">{cards}
        </div>
      </div>
    </section>"""

svc_nav = '\n        <div class="svc-nav">' + "".join(
    f'<a href="#{sid}">{title}</a>' for sid, _, title, _, _ in SERVICES) + "</div>"
services = page_hero("Our Services", "Electrical services, air conditioning installation, and air conditioning servicing, maintenance &amp; repairs.", svc_nav, "page-services.jpg") + svc_sections + f"""

    <section id="work">
      <div class="container">
        <div class="center">
          <h2 class="section-title">Our Recent Work</h2>
          <p class="section-intro">Real jobs completed by Tony for homes and businesses across Sydney.</p>
        </div>
        <div class="work-grid">{gallery(WORK)}
        </div>
      </div>
    </section>

""" + CTA

# ---------- About ----------
about = page_hero("About Us", "The best &amp; trusted in North Sydney.", photo="page-about.jpg") + f"""

    <section>
      <div class="container about-grid">
        <div class="about-text">
          <h2 class="section-title" style="margin-bottom:22px">HTB Electrical &amp; Air Conditioning</h2>
          <p class="tagline">The best &amp; trusted in North Sydney.</p>
          <p>HTB Electrical &amp; Air Conditioning is a family-owned electrical and air conditioning business located in North Sydney. We provide installation, servicing, maintenance and repairs for homes and businesses.</p>
          <p>Because we are both qualified electricians and air conditioning technicians, we can look after the whole job – from the power supply to the finished installation – with one call.</p>
          <p>We provide electrical services and air conditioning installation Sydney wide, including the Sydney CBD, Lower North Shore, Northern Beaches, Ryde District, Inner West, Hills District and Eastern Suburbs.</p>
          <div class="hero-actions" style="margin-top:24px">
            <a href="quote.html" class="btn btn-red">Get a Free Quote</a>
            <a href="{TEL}" class="btn btn-navy-outline">{ico("phone")}Call {PHONE}</a>
          </div>
        </div>
        <div class="profile">
          <img class="profile-photo" src="images/about-tony.jpg" alt="Tony Bui, owner of HTB Electrical &amp; Air Conditioning, after installing a feature light" width="800" height="1000">
          <h3>Tony Bui</h3>
          <p class="role">Owner · Qualified Electrician &amp; Air Conditioning Technician</p>
          <p class="about-tony">Tony is a qualified electrician and air conditioning technician with more than 10 years of experience. He founded HTB Electrical &amp; Air Conditioning to give Sydney families the honest, reliable service he’d want for his own home. Tony looks after every job personally, from small repairs to full installations, and takes pride in clear communication, fair pricing and leaving every home clean and tidy.</p>
        </div>
      </div>
    </section>

    <section class="bg-soft">
      <div class="container">
        <div class="values">
          <div class="value">
            <div class="icon-wrap">{ico("family")}</div>
            <div><h3>Family Owned</h3><p>A local North Sydney business that cares about every job.</p></div>
          </div>
          <div class="value">
            <div class="icon-wrap">{ico("bolt")}</div>
            <div><h3>Fast, Local &amp; Reliable</h3><p>Available 24 hours a day, 7 days a week.</p></div>
          </div>
          <div class="value">
            <div class="icon-wrap">{ico("shield")}</div>
            <div><h3>Licensed &amp; Insured</h3><p>Electrical Licence No. {LICENCE}.</p></div>
          </div>
        </div>
      </div>
    </section>

{CTA}"""

# ---------- Locations ----------
region_cards = "".join(f"""
          <div class="region">
            <h3>{ico("pin")}{name}</h3>
            <ul class="chips">{"".join(f"<li>{s}</li>" for s in subs)}</ul>
          </div>""" for name, subs in REGIONS)
locations = page_hero("Areas We Service", "Electrical and air conditioning services Sydney wide.", photo="page-locations.jpg") + f"""

    <section>
      <div class="container">
        <p class="loc-intro">Our office is located in <strong>North Sydney</strong>, but HTB Electrical &amp; Air Conditioning provides electrical services and air conditioning installation <strong>Sydney wide</strong>, including the Sydney CBD, Lower North Shore, Northern Beaches, Ryde District, Inner West, Hills District and Eastern Suburbs of Sydney.</p>
      </div>
    </section>

    <section class="bg-soft" style="padding-top:48px">
      <div class="container">
        <div class="region-grid">{region_cards}
        </div>
        <p class="center" style="margin-top:32px;font-size:1.1rem">Don't see your suburb? <a href="{TEL}"><strong>Call us on {PHONE}</strong></a> – we work all over Sydney.</p>
      </div>
    </section>

{CTA}"""

# ---------- Contact ----------
contact = page_hero("Contact Us", "We're always happy to hear from you.", photo="page-contact.jpg") + f"""

    <section>
      <div class="container contact-grid">
        <div>
          <p class="big-text">Give us a call or send us your enquiry. <strong>We'll get back to you within 48 hours.</strong></p>
          <div class="contact-lines">
            <a class="contact-line" href="{TEL}">
              <div class="icon-wrap">{ico("phone")}</div>
              <div><div class="label">Phone – 24/7</div><div class="value">{PHONE}</div></div>
            </a>
            <a class="contact-line" href="mailto:{EMAIL}">
              <div class="icon-wrap">{ico("mail")}</div>
              <div><div class="label">Email</div><div class="value">{EMAIL}</div></div>
            </a>
            <div class="contact-line">
              <div class="icon-wrap">{ico("clock")}</div>
              <div><div class="label">Open hours</div><div class="value">24 hours, 7 days</div></div>
            </div>
          </div>
          <a href="quote.html" class="btn btn-red">Request a quote or booking here</a>
          <div class="map">
            <iframe src="https://maps.google.com/maps?q=HTB%20ELECTRICAL%20%26%20AIR%20CONDITIONING%20P%2FL%2C%20North%20Sydney%20NSW&amp;z=13&amp;output=embed" title="HTB Electrical &amp; Air Conditioning on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
          </div>
          <a class="btn btn-navy-outline map-btn" href="{GOOGLE_PROFILE}" target="_blank" rel="noopener">{ico("pin")}Open in Google Maps</a>
        </div>
        <div>
          {short_form("c", "Get a Booking or Quote", "Send us your details and we'll be in touch.", "New booking/quote request – website (contact page)", "form-card flat")}
        </div>
      </div>
    </section>"""

# ---------- Quote ----------
quote_page = page_hero("Get a Quote or Booking", "Simply fill out the details below and we will be in contact with you as soon as we can.") + f"""

    <section>
      <div class="container quote-grid">
        <form class="form-card flat" action="{FORM_ACTION}" method="POST" enctype="multipart/form-data">
          {hidden_fields("New quote/booking request – website")}
          <h2>Your Details</h2>
          <p class="hint">Fields marked optional can be left blank.</p>
          <div class="field">
            <label for="q-name">Full name</label>
            <input id="q-name" name="name" type="text" autocomplete="name" required>
          </div>
          <div class="form-row">
            <div class="field">
              <label for="q-phone">Phone</label>
              <input id="q-phone" name="phone" type="tel" autocomplete="tel" required>
            </div>
            <div class="field">
              <label for="q-email">Email</label>
              <input id="q-email" name="email" type="email" autocomplete="email" required>
            </div>
          </div>
          <div class="field">
            <label for="q-address">Address</label>
            <input id="q-address" name="address" type="text" autocomplete="street-address" required>
          </div>
          <div class="field">
            <label for="q-service">Service needed</label>
            {service_select().replace("{p}", "q")}
          </div>
          <div class="field">
            <label for="q-message">How can we help?</label>
            <textarea id="q-message" name="message" placeholder="Enter a description of the work you would like to do" required></textarea>
          </div>
          <div class="field">
            <label for="q-file">Attachment <span class="opt">(optional)</span></label>
            <input id="q-file" name="attachment" type="file" accept="image/*,.pdf">
            <p class="help">Please attach a photo or document that will help describe your job (max 5 MB).</p>
          </div>
          <button type="submit" class="btn btn-red btn-block">Submit</button>
        </form>

        <aside class="side-panel">
          <h2>Get in touch with our team today</h2>
          <p>We're always happy to hear from you.</p>
          <a class="line" href="{TEL}">{ico("phone")}<span><small>Call us on</small>{PHONE}</span></a>
          <a class="line" href="mailto:{EMAIL}">{ico("mail")}<span><small>Email</small>{EMAIL}</span></a>
          <p class="line" style="display:flex;gap:12px;align-items:center;font-weight:700;margin:0">{ico("clock")}<span><small>Open hours</small>24 hours, 7 days</span></p>
        </aside>
      </div>
    </section>"""

# ---------- Thanks ----------
thanks = page_hero("Thank You!", "Your request has been sent.") + f"""

    <section>
      <div class="container center">
        <p class="big-text" style="margin-bottom:24px">We've received your details and will be in contact with you as soon as we can.<br>For anything urgent, please call us now.</p>
        <div class="hero-actions" style="justify-content:center">
          <a href="{TEL}" class="btn btn-red">{ico("phone")}Call {PHONE}</a>
          <a href="index.html" class="btn btn-navy-outline">Back to Home</a>
        </div>
      </div>
    </section>"""

D = "HTB Electrical & Air Conditioning Pty Ltd – family-owned North Sydney electricians and air conditioning technicians, available 24/7. Lic. " + LICENCE + "."
PAGES = [
    ("index.html", "HTB Electrical &amp; Air Conditioning | North Sydney Electrician &amp; Air Con", D, home, "index.html"),
    ("services.html", "Our Services | HTB Electrical &amp; Air Conditioning", "Electrical services, split system air conditioning installation, and air conditioning servicing and repairs across Sydney.", services, "services.html"),
    ("about.html", "About Us | HTB Electrical &amp; Air Conditioning", "Family-owned electrical and air conditioning business located in North Sydney.", about, "about.html"),
    ("locations.html", "Areas We Service | HTB Electrical &amp; Air Conditioning", "Electrician and air conditioning installation in North Sydney, Sydney CBD, Lower North Shore, Northern Beaches, Ryde, Inner West, Hills District and Eastern Suburbs.", locations, "locations.html"),
    ("contact.html", "Contact Us | HTB Electrical &amp; Air Conditioning", "Call HTB Electrical & Air Conditioning 24/7 on " + PHONE + " or send us your enquiry.", contact, "contact.html"),
    ("quote.html", "Get a Quote or Booking | HTB Electrical &amp; Air Conditioning", "Request a free quote or booking from HTB Electrical & Air Conditioning.", quote_page, None),
    ("thanks.html", "Thank You | HTB Electrical &amp; Air Conditioning", "Thank you for your enquiry.", thanks, None),
]
for fn, title, desc, body, active in PAGES:
    with open(os.path.join(OUT, fn), "w") as f:
        f.write(page(fn, title, desc, body, active))
print("built", len(PAGES), "pages")
