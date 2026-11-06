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
