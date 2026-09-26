// Restrained, functional motion: sections below the fold rise into place once, chart bars grow
// in from zero the first time their figure is on screen, and the nav tracks which in-page section
// (Work / Experience) is current while scrolling the home page.
//
// Progressive enhancement: every element this script touches is fully visible in plain CSS
// without it (see the "motion" block in site.css). With JS disabled, or reduced motion requested,
// nothing below runs and the page is unaffected.
(function () {
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!("IntersectionObserver" in window)) return;
  document.documentElement.classList.add("js-motion");

  function revealOnce(selector, className, options) {
    var targets = document.querySelectorAll(selector);
    if (!targets.length) return;
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add(className);
        observer.unobserve(entry.target);
      });
    }, options);
    targets.forEach(function (el) { observer.observe(el); });
  }

  revealOnce(".section, .now", "is-visible", { threshold: 0.08, rootMargin: "0px 0px -8% 0px" });
  revealOnce(".chart", "is-charted", { threshold: 0.2 });

  // Nav scroll-spy: only the home page has #work / #experience anchors in the nav, so this is a
  // no-op (nothing found) on every other page.
  var navLinks = {};
  document.querySelectorAll('.topbar nav a[href*="#work"], .topbar nav a[href*="#experience"]').forEach(function (a) {
    var id = a.getAttribute("href").split("#")[1];
    if (id) navLinks[id] = a;
  });
  var ids = Object.keys(navLinks);
  if (!ids.length) return;
  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var link = navLinks[entry.target.id];
      if (!link || !entry.isIntersecting) return;
      ids.forEach(function (id) { navLinks[id].removeAttribute("aria-current"); });
      link.setAttribute("aria-current", "true");
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  ids.forEach(function (id) {
    var el = document.getElementById(id);
    if (el) spy.observe(el);
  });
})();
