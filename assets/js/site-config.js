/* MeasureStack — single configuration point (temporary working brand).
   Portability: set SITE_URL once on deploy. BASE_PATH "/money/" for project
   site; change to "/" for user site or custom domain. No USERNAME hardcoded
   except inside SITE_URL which you edit once. */
window.SITE = window.SITE || {
  NAME: "MeasureStack",
  TAGLINE: "How much material do I need?",
  SITE_URL: "https://rayanbaig796-crypto.github.io/money",
  BASE_PATH: "/money/"
};
(function () {
  // Safe storage wrapper (try/catch, falls back silently)
  window.safeStore = {
    get: function (k, fb) {
      try { var v = localStorage.getItem(k); return v === null ? fb : v; }
      catch (e) { return fb; }
    },
    set: function (k, v) {
      try { localStorage.setItem(k, v); } catch (e) { /* unavailable: ignore */ }
    }
  };
  // Apply brand name to non-SEO-critical UI slots only.
  // SEO-critical title/H1/meta are static in HTML per page (do not inject).
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-brand]").forEach(function (el) {
      el.textContent = window.SITE.NAME;
    });
  });
})();
