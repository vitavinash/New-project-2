(() => {
  "use strict";
  if (window.lucide) window.lucide.createIcons();
  const body = document.body;
  const themeButton = document.getElementById("theme-toggle");
  try {
    body.classList.toggle(
      "dark",
      localStorage.getItem("smarteye-theme") === "dark",
    );
  } catch (_) {}
  const themeLabel = () => {
    const label = body.classList.contains("dark")
      ? "Switch to light theme"
      : "Switch to dark theme";
    themeButton?.setAttribute("aria-label", label);
    themeButton?.setAttribute("title", label);
  };
  themeLabel();
  themeButton?.addEventListener("click", () => {
    body.classList.toggle("dark");
    try {
      localStorage.setItem(
        "smarteye-theme",
        body.classList.contains("dark") ? "dark" : "light",
      );
    } catch (_) {}
    themeLabel();
  });
  const menu = document.getElementById("primary-nav");
  const menuButton = document.getElementById("menu-toggle");
  const closeMenu = () => {
    menu?.classList.remove("open");
    menuButton?.setAttribute("aria-expanded", "false");
  };
  menuButton?.addEventListener("click", () => {
    const open = menu.classList.toggle("open");
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute(
      "aria-label",
      open ? "Close navigation" : "Open navigation",
    );
  });
  menu
    ?.querySelectorAll("a")
    .forEach((a) => a.addEventListener("click", closeMenu));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && menu?.classList.contains("open")) {
      closeMenu();
      menuButton.focus();
    }
  });
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".site-header")) closeMenu();
  });
  const toast = document.getElementById("toast");
  let toastTimer;
  function notify(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.hidden = true;
    }, 4000);
  }
  const dataElement = document.getElementById("trace-data");
  if (dataElement) {
    const records = JSON.parse(dataElement.textContent);
    let selected = 0;
    let stage = "need";
    const rows = [...document.querySelectorAll("[data-trace-index]")];
    const stageButtons = [...document.querySelectorAll("[data-stage]")];
    function inspect() {
      const record = records[selected];
      const descriptions = {
        need: record.need_text,
        req: record.req_text,
        risk: record.risk_text + " Control: " + record.mitigation,
        test:
          "Verification protocol " + record.test_id + ": " + record.test_status,
        evidence: "Sample release evidence linked to " + record.test_id + ".",
      };
      document.getElementById("trace-record-id").textContent =
        record[stage + "_id"];
      document.getElementById("trace-record-text").textContent =
        descriptions[stage];
      document.getElementById("trace-record-status").textContent =
        stage === "test" ? record.test_status : "Connected";
      stageButtons.forEach((button) => {
        const active = button.dataset.stage === stage;
        button.classList.toggle("active", active);
        button.setAttribute("aria-pressed", String(active));
      });
      rows.forEach((row) =>
        row.classList.toggle(
          "selected",
          Number(row.dataset.traceIndex) === selected,
        ),
      );
    }
    stageButtons.forEach((button) =>
      button.addEventListener("click", () => {
        stage = button.dataset.stage;
        inspect();
      }),
    );
    document.querySelectorAll(".inspect-record").forEach((button) =>
      button.addEventListener("click", () => {
        selected = Number(button.dataset.index);
        inspect();
        document
          .querySelector(".trace-inspector")
          .scrollIntoView({
            behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
              ? "instant"
              : "smooth",
            block: "center",
          });
      }),
    );
    document.getElementById("trace-search").addEventListener("input", (e) => {
      const query = e.target.value.trim().toLowerCase();
      rows.forEach((row) => {
        row.hidden = !Object.values(records[Number(row.dataset.traceIndex)])
          .join(" ")
          .toLowerCase()
          .includes(query);
      });
      const visible = rows.filter((row) => !row.hidden);
      document.getElementById("trace-count").textContent =
        visible.length + (visible.length === 1 ? " record" : " records");
      document.getElementById("trace-empty").hidden = visible.length > 0;
      document.getElementById("export-trace").disabled = visible.length === 0;
      if (visible.length) {
        selected = Number(visible[0].dataset.traceIndex);
        inspect();
      }
    });
    document.getElementById("export-trace").addEventListener("click", () => {
      const fields = [
        "need_id",
        "need_text",
        "req_id",
        "req_text",
        "risk_id",
        "risk_text",
        "mitigation",
        "test_id",
        "test_status",
        "evidence_id",
      ];
      const quote = (value) =>
        '"' + String(value ?? "").replaceAll('"', '""') + '"';
      const filtered = rows
        .filter((row) => !row.hidden)
        .map((row) => records[Number(row.dataset.traceIndex)]);
      const csv = [
        fields.map(quote).join(","),
        ...filtered.map((record) =>
          fields.map((key) => quote(record[key])).join(","),
        ),
      ].join("\r\n");
      const url = URL.createObjectURL(
        new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" }),
      );
      const link = document.createElement("a");
      link.href = url;
      link.download = "smarteye-sample-traceability.csv";
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      notify("Sample traceability CSV downloaded.");
    });
    inspect();
  }
  const deviceTabs = [...document.querySelectorAll("[data-device]")];
  function selectDevice(tab) {
    deviceTabs.forEach((button) => {
      const active = button === tab;
      button.classList.toggle("active", active);
      button.setAttribute("aria-selected", String(active));
      button.tabIndex = active ? 0 : -1;
      document.getElementById("device-" + button.dataset.device).hidden =
        !active;
    });
  }
  deviceTabs.forEach((tab, index) => {
    tab.addEventListener("click", () => selectDevice(tab));
    tab.addEventListener("keydown", (e) => {
      let target;
      if (["ArrowDown", "ArrowRight"].includes(e.key))
        target = (index + 1) % deviceTabs.length;
      if (["ArrowUp", "ArrowLeft"].includes(e.key))
        target = (index - 1 + deviceTabs.length) % deviceTabs.length;
      if (e.key === "Home") target = 0;
      if (e.key === "End") target = deviceTabs.length - 1;
      if (target !== undefined) {
        e.preventDefault();
        selectDevice(deviceTabs[target]);
        deviceTabs[target].focus();
      }
    });
  });
  document.querySelectorAll("[data-interest]").forEach((link) =>
    link.addEventListener("click", () => {
      const interest = document.getElementById("id_interest");
      if (interest) {
        interest.value = link.dataset.interest;
        notify("Selected: " + link.dataset.interest);
      }
    }),
  );
  const calculatorInputs = ["roi-team", "roi-hours", "roi-reduction"].map(
    (id) => document.getElementById(id),
  );
  if (calculatorInputs.every(Boolean)) {
    const recalculate = () => {
      const values = calculatorInputs.map((input) =>
        Math.min(
          Number(input.max),
          Math.max(Number(input.min), Number(input.value) || 0),
        ),
      );
      const weekly = (values[0] * values[1] * values[2]) / 100;
      document.getElementById("roi-percent").textContent = values[2] + "%";
      document.getElementById("roi-weekly").textContent = weekly.toLocaleString(
        undefined,
        { maximumFractionDigits: 1 },
      );
      document.getElementById("roi-yearly").textContent = Math.round(
        weekly * 52,
      ).toLocaleString();
    };
    calculatorInputs.forEach((input) => {
      input.addEventListener("input", recalculate);
      input.addEventListener("change", () => {
        input.value = Math.min(
          Number(input.max),
          Math.max(Number(input.min), Number(input.value) || 0),
        );
        recalculate();
      });
    });
    recalculate();
  }
  document.getElementById("show-password")?.addEventListener("click", (e) => {
    const password = document.getElementById("password");
    const show = password.type === "password";
    password.type = show ? "text" : "password";
    e.currentTarget.setAttribute(
      "aria-label",
      show ? "Hide password" : "Show password",
    );
    e.currentTarget.setAttribute("aria-pressed", String(show));
  });
  const dialog = document.getElementById("action-dialog");
  document
    .querySelectorAll("[data-open-action]")
    .forEach((button) =>
      button.addEventListener("click", () => dialog.showModal()),
    );
  document
    .querySelectorAll("[data-close-dialog]")
    .forEach((button) =>
      button.addEventListener("click", () => dialog.close()),
    );
  if (dialog?.dataset.errors === "true") dialog.showModal();
  document.querySelectorAll("form[method='post']").forEach((form) =>
    form.addEventListener("submit", () => {
      const button = form.querySelector("button[type='submit']");
      if (button) {
        button.disabled = true;
        button.setAttribute("aria-busy", "true");
      }
    }),
  );
  window.addEventListener("pageshow", () =>
    document.querySelectorAll("button[aria-busy='true']").forEach((button) => {
      button.disabled = false;
      button.removeAttribute("aria-busy");
    }),
  );
  const error = document.querySelector("#lead-form .form-error");
  if (error) error.focus();
})();
