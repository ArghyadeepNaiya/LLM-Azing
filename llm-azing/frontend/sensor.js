const ThreatShield = {
  telemetry: {
    mouseMovements: 0,
    scrollDepth: 0,
    timeOnPage: 0,
    isTrustedEvent: true, // NEW: Checks for physical hardware click
    canvasHash: null, // NEW: GPU Fingerprint
    memoryLeaks: false, // NEW: Scans for Selenium variables
  },

  startTime: Date.now(),

  init: function () {
    console.log("🛡️ ThreatShield Level 3: Advanced Biometrics Active.");

    this.generateGPUFingerprint();
    this.scanMemoryForAutomation();

    document.addEventListener("mousemove", (e) => {
      this.telemetry.mouseMovements++;
      document.getElementById("ui-mouse").innerText =
        this.telemetry.mouseMovements + " events";

      const hudX = document.getElementById("hud-x");
      const hudY = document.getElementById("hud-y");
      if (hudX && hudY) {
        hudX.innerText = e.clientX;
        hudY.innerText = e.clientY;
      }
    });

    document.addEventListener("scroll", () => {
      let scrollTop = Math.round(
        window.scrollY || document.documentElement.scrollTop,
      );
      if (scrollTop > this.telemetry.scrollDepth) {
        this.telemetry.scrollDepth = scrollTop;
        document.getElementById("ui-scroll").innerText = scrollTop + " px";
      }
    });

    setInterval(() => {
      this.telemetry.timeOnPage = Math.floor(
        (Date.now() - this.startTime) / 1000,
      );
      document.getElementById("ui-time").innerText =
        this.telemetry.timeOnPage + "s";
    }, 1000);

    document.addEventListener("DOMContentLoaded", () => {
      this.attachToScraperTraps();
    });
  },

  // --- ADVANCED DETECTION METHODS ---

  generateGPUFingerprint: function () {
    // Silently draws a complex graphic and hashes the pixel data.
    // Headless cloud servers render this differently than real GPUs.
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    ctx.textBaseline = "top";
    ctx.font = "14px Arial";
    ctx.fillStyle = "#f60";
    ctx.fillRect(125, 1, 62, 20);
    ctx.fillStyle = "#069";
    ctx.fillText("ThreatShield AI", 2, 15);

    const dataURI = canvas.toDataURL();
    let hash = 0;
    for (let i = 0; i < dataURI.length; i++) {
      hash = (hash << 5) - hash + dataURI.charCodeAt(i);
      hash = hash & hash;
    }
    this.telemetry.canvasHash = hash.toString();
    console.log("🛡️ GPU Fingerprint generated.");
  },

  scanMemoryForAutomation: function () {
    // Scans the browser's hidden memory for Selenium artifacts
    for (let key in window) {
      if (key.startsWith("cdc_") || key === "webdriver") {
        this.telemetry.memoryLeaks = true;
      }
    }
  },

  attachToScraperTraps: function () {
    const buttons = document.querySelectorAll(".trap-btn");
    buttons.forEach((btn) => {
      btn.addEventListener("click", async (e) => {
        // THE ULTIMATE TRAP: Check if a physical mouse clicked this, or a script.
        this.telemetry.isTrustedEvent = e.isTrusted;

        document.getElementById("status-text").innerText =
          "Analyzing deep telemetry...";

        try {
          let response = await fetch("http://localhost:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.telemetry),
          });

          let result = await response.json();

          if (result.is_bot) {
            document.getElementById("status-text").innerText =
              "🚨 DOM INJECTION BLOCKED 🚨";
            document.getElementById("status-display").style.borderColor =
              "#ef4444";
            document.getElementById("status-text").style.color = "#ef4444";
            btn.disabled = true;
          } else {
            document.getElementById("status-text").innerText =
              "✅ HARDWARE VERIFIED";
          }
        } catch (error) {
          console.error("API Error:", error);
        }
      });
    });
  },
};

ThreatShield.init();
