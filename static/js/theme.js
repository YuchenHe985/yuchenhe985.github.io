// Three-state theme switch: system (no attribute) -> light -> dark -> system.
(function () {
  var root = document.documentElement;
  var button = document.getElementById("theme-toggle");
  if (!button) return;
  var order = ["system", "light", "dark"];
  function current() {
    var t = root.getAttribute("data-theme");
    return t === "light" || t === "dark" ? t : "system";
  }
  function show() {
    var name = current();
    button.textContent = name.charAt(0).toUpperCase() + name.slice(1);
    button.setAttribute("aria-label", "Colour theme: " + name + ". Activate to change.");
  }
  button.addEventListener("click", function () {
    var next = order[(order.indexOf(current()) + 1) % order.length];
    if (next === "system") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", next);
    try {
      if (next === "system") localStorage.removeItem("theme");
      else localStorage.setItem("theme", next);
    } catch (e) {}
    show();
  });
  show();
})();
