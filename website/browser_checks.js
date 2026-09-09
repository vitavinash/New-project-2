(async () => {
  const results = [];
  const check = (name, condition) => {
    if (!condition) throw new Error(name);
    results.push(name);
  };
  const input = (id, value) => {
    const el = document.getElementById(id);
    el.value = value;
    el.dispatchEvent(new Event("input", { bubbles: true }));
  };
  check(
    "Page fits viewport",
    document.documentElement.scrollWidth <= innerWidth,
  );
  check(
    "Hero image loaded",
    document.querySelector(".hero-photo").naturalWidth > 0,
  );
  check("Icons rendered", document.querySelectorAll("svg.lucide").length > 20);
  input("trace-search", "SRS-518");
  check(
    "Search filters records",
    document.querySelectorAll("[data-trace-index]:not([hidden])").length === 1,
  );
  document.querySelector("[data-stage='risk']").click();
  check(
    "Inspector follows selected record",
    document.getElementById("trace-record-id").textContent === "HAZ-104",
  );
  input("trace-search", "no-such-record");
  check(
    "Empty search state",
    !document.getElementById("trace-empty").hidden &&
      document.getElementById("export-trace").disabled,
  );
  input("trace-search", "");
  check(
    "Search reset",
    document.querySelectorAll("[data-trace-index]:not([hidden])").length === 3,
  );
  const originalCreate = URL.createObjectURL;
  let csvText;
  URL.createObjectURL = (blob) => {
    csvText = blob.text();
    return originalCreate(blob);
  };
  document.getElementById("export-trace").click();
  URL.createObjectURL = originalCreate;
  const csv = await csvText;
  check(
    "Trace CSV contains all records",
    csv.includes("UN-102") &&
      csv.includes("UN-105") &&
      csv.includes("UN-114") &&
      csv.split("\r\n").length === 4,
  );
  document.querySelector("[data-device='ivd']").click();
  check(
    "Device tab switches panel",
    !document.getElementById("device-ivd").hidden &&
      document.getElementById("device-samd").hidden,
  );
  document.querySelector("#device-ivd [data-interest]").click();
  check(
    "Consultation interest prefilled",
    document.getElementById("id_interest").value.includes("In Vitro"),
  );
  input("roi-team", "10");
  input("roi-hours", "5");
  input("roi-reduction", "50");
  check(
    "Calculator updates",
    document.getElementById("roi-weekly").textContent === "25" &&
      document.getElementById("roi-yearly").textContent.replaceAll(",", "") ===
        "1300",
  );
  const theme = document.body.classList.contains("dark");
  document.getElementById("theme-toggle").click();
  check("Theme switches", document.body.classList.contains("dark") !== theme);
  document.getElementById("theme-toggle").click();
  if (innerWidth <= 800) {
    document.getElementById("menu-toggle").click();
    check(
      "Mobile menu opens",
      document.getElementById("menu-toggle").getAttribute("aria-expanded") ===
        "true",
    );
    document.dispatchEvent(
      new KeyboardEvent("keydown", { key: "Escape", bubbles: true }),
    );
    check(
      "Escape closes menu",
      document.getElementById("menu-toggle").getAttribute("aria-expanded") ===
        "false",
    );
  }
  input("roi-team", "8");
  input("roi-hours", "6");
  input("roi-reduction", "30");
  document.querySelector("[data-device='samd']").click();
  document.querySelector("[data-stage='need']").click();
  document.getElementById("id_interest").value = "";
  history.replaceState(null, "", "/");
  window.scrollTo({ top: 0, behavior: "instant" });
  return { viewport: innerWidth, passed: results };
})();
