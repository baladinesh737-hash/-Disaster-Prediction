/**
 * script.js – Legacy shim
 * All dashboard logic is now in api.js (shared) and inline per-page scripts.
 * This file is kept for backward compatibility only.
 */

// Redirect old entry point to new index
if (
  window.location.pathname.endsWith("script.js") === false &&
  document.getElementById("map") &&
  typeof initLeafletMap === "function"
) {
  // If an old page loads this, initialize a basic map
  window.addEventListener("DOMContentLoaded", function () {
    const mapEl = document.getElementById("map");
    if (mapEl && typeof L !== "undefined") {
      initLeafletMap("map");
    }
  });
}
