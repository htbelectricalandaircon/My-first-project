// Mobile menu
var menuBtn = document.getElementById("menu-btn");
var navLinks = document.getElementById("nav-links");
menuBtn.addEventListener("click", function () {
  var open = navLinks.classList.toggle("open");
  menuBtn.setAttribute("aria-expanded", open);
});

// Floating call button appears once the visitor scrolls down
var floatBtn = document.getElementById("call-float");
function updateFloat() {
  floatBtn.classList.toggle("show", window.scrollY > 450);
}
window.addEventListener("scroll", updateFloat, { passive: true });
updateFloat();

// Pre-select the service when arriving from a "Get a quote" button (quote.html?service=...)
var serviceParam = new URLSearchParams(window.location.search).get("service");
if (serviceParam) {
  document.querySelectorAll("select[name='service']").forEach(function (select) {
    Array.prototype.forEach.call(select.options, function (opt) {
      if (opt.value === serviceParam) select.value = serviceParam;
    });
  });
}

// Check the size of the attached file before sending
document.querySelectorAll("input[type='file']").forEach(function (input) {
  input.addEventListener("change", function () {
    var total = 0;
    Array.prototype.forEach.call(input.files, function (f) { total += f.size; });
    if (total > 5 * 1024 * 1024) {
      alert("This file is too large (max 5 MB). Please choose a smaller photo or document.");
      input.value = "";
    }
  });
});

document.getElementById("year").textContent = new Date().getFullYear();

// Lead events for Google Tag Manager. These do nothing until a GTM container is installed.
window.dataLayer = window.dataLayer || [];
document.addEventListener("click", function (e) {
  var link = e.target.closest ? e.target.closest("a[href^='tel:'], a[href^='mailto:']") : null;
  if (!link) return;
  var isPhone = link.getAttribute("href").indexOf("tel:") === 0;
  window.dataLayer.push({ event: isPhone ? "phone_click" : "email_click", page_path: window.location.pathname });
});
document.querySelectorAll("form[action*='formsubmit.co']").forEach(function (form) {
  form.addEventListener("submit", function () {
    var service = form.querySelector("select[name='service']");
    try {
      sessionStorage.setItem("htb_lead", JSON.stringify({ form_page: window.location.pathname, service: service ? service.value : "" }));
    } catch (err) {}
  });
});
// Only count a lead when this browser tab really submitted a form, so direct visits to the thank-you page are ignored.
if (/\/thanks(\.html)?$/.test(window.location.pathname)) {
  try {
    var lead = sessionStorage.getItem("htb_lead");
    if (lead) {
      sessionStorage.removeItem("htb_lead");
      var details = JSON.parse(lead);
      window.dataLayer.push({ event: "generate_lead", form_page: details.form_page, service: details.service });
    }
  } catch (err) {}
}
