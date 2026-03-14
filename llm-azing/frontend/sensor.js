const ThreatShield = {
  telemetry: {
    mouseMovements: 0,
    scrollDepth: 0,
    timeOnPage: 0,
    linearityScore: 0, // NEW: Detects if movement is too "perfect"
    lastCoords: null,
  },

  movementLog: [],
  startTime: Date.now(),

  init: function () {
    document.addEventListener("mousemove", (e) => {
      this.telemetry.mouseMovements++;

      // KINEMATIC ANALYSIS: Check for straight lines
      if (this.telemetry.lastCoords) {
        const dx = e.clientX - this.telemetry.lastCoords.x;
        const dy = e.clientY - this.telemetry.lastCoords.y;
        const angle = Math.atan2(dy, dx);
        this.movementLog.push(angle);

        // If the last 10 angles are identical, it's a straight line (Bot)
        if (this.movementLog.length > 10) {
          this.movementLog.shift();
          const isLinear = this.movementLog.every(
            (a) => a === this.movementLog[0],
          );
          if (isLinear) this.telemetry.linearityScore++;
        }
      }
      this.telemetry.lastCoords = { x: e.clientX, y: e.clientY };

      // Update HUD
      document.getElementById("hud-x").innerText = e.clientX;
      document.getElementById("hud-y").innerText = e.clientY;
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

  attachToScraperTraps: function () {
    const buttons = document.querySelectorAll(".trap-btn");
    buttons.forEach((btn) => {
      btn.addEventListener("click", async () => {
        document.getElementById("status-text").innerText =
          "Analyzing Kinematics...";
        try {
          let response = await fetch("http://localhost:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.telemetry),
          });
          let result = await response.json();
          if (result.is_bot) {
            document.getElementById("status-text").innerText =
              "🚨 ADVANCED BOT BLOCKED 🚨";
            document.getElementById("status-display").style.borderColor =
              "#ef4444";
            btn.disabled = true;
          } else {
            document.getElementById("status-text").innerText =
              "✅ HUMAN VERIFIED";
          }
        } catch (e) {
          console.error(e);
        }
      });
    });
  },
};
ThreatShield.init();
