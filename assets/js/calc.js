/* Shared calc helpers: validation, unit conversion via SI base, rounding. */
(function () {
  "use strict";
  var store = window.safeStore || { get: function (k, fb) { return fb; }, set: function () {} };
  var FT = 0.3048, IN = 0.0254, YD3 = 0.764554857984, SQFT = 0.09290304;

  window.Calc = {
    unitSystem: function (fallback) {
      var u = store.get("ms-units", fallback || "imperial");
      return (u === "metric") ? "metric" : "imperial";
    },
    setUnits: function (u) { store.set("ms-units", u); },
    // length inputs -> meters
    lenToM: function (v, unit) {
      v = Number(v);
      if (!isFinite(v)) return NaN;
      if (unit === "ft") return v * FT;
      if (unit === "in") return v * IN;
      if (unit === "m") return v;
      if (unit === "cm") return v / 100;
      if (unit === "mm") return v / 1000;
      return v * FT;
    },
    m3ToYd3: function (m3) { return m3 / YD3; },
    m3ToCuFt: function (m3) { return m3 * 35.314666721; },
    m2ToSqFt: function (m2) { return m2 / SQFT; },
    num: function (v, name) {
      v = Number(v);
      if (v === "" || v === null || !isFinite(v)) throw new Error("Enter a valid number for " + name + ".");
      return v;
    },
    nonNeg: function (v, name) {
      v = this.num(v, name);
      if (v < 0) throw new Error(name + " cannot be negative.");
      return v;
    },
    roundUp: function (v) { return Math.ceil(v - 1e-9); },
    fmt: function (v, d) {
      if (!isFinite(v)) return "—";
      return Number(v).toLocaleString("en-US", { maximumFractionDigits: (d === undefined ? 2 : d) });
    },
    show: function (el, html, isErr) {
      el.classList.remove("error");
      if (isErr) el.classList.add("error");
      el.innerHTML = html;
      el.setAttribute("role", isErr ? "alert" : "status");
    },
    bindUnits: function (rootId, onChange) {
      var root = document.getElementById(rootId);
      if (!root) return "imperial";
      var cur = this.unitSystem("imperial");
      function paint() {
        root.querySelectorAll("button[data-u]").forEach(function (b) {
          b.setAttribute("aria-pressed", b.dataset.u === cur ? "true" : "false");
        });
        // Labels live throughout the form (not inside #units), so query document-wide.
        document.querySelectorAll("[data-unit-label]").forEach(function (s) {
          var imp = s.getAttribute("data-imp"), met = s.getAttribute("data-met");
          s.textContent = (cur === "metric") ? met : imp;
        });
      }
      root.addEventListener("click", function (e) {
        var b = e.target.closest("button[data-u]");
        if (!b) return;
        cur = b.dataset.u; window.Calc.setUnits(cur); paint(); if (onChange) onChange(cur);
      });
      paint();
      return cur;
    }
  };
})();
