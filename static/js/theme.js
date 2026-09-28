// Three-state theme switch: system -> light -> dark -> system, localized to the page language.
(function () {
  var root = document.documentElement;
  var button = document.getElementById("theme-toggle");
  if (!button) return;

  var order = ["system", "light", "dark"];
  var zh = root.lang === "zh";
  var labels = zh
    ? { system: "跟随系统", light: "浅色", dark: "深色" }
    : { system: "System", light: "Light", dark: "Dark" };

  function current() {
    var t = root.getAttribute("data-theme");
    return t === "light" || t === "dark" ? t : "system";
  }

  function show() {
    var name = current();
    button.textContent = labels[name];
    button.setAttribute(
      "aria-label",
      zh
        ? "当前配色：" + labels[name] + "。点击切换。"
        : "Color theme: " + name + ". Activate to change."
    );
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
