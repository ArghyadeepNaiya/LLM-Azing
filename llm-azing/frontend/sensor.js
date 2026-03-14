const ThreatShield = {
  telemetry: {
    mouseMovements: 0,
    scrollDepth: 0,
    timeOnPage: 0,
    linearityScore: 0,
    resizeEvents: 0,
    pollingRate: 0,
    typingRhythm: 0,   
    browserEntropy: 0, 
    requestTiming: 0,  
    
    lastCoords: null,
    lastMouseTime: 0,
    mouseIntervals: [],
    keyIntervals: [],
    lastKeyTime: 0
  },

  movementLog: [],
  startTime: performance.now(),

  init: function () {
    // 1. Wrap DOM interactions in an event listener so it doesn't crash before HTML loads
    document.addEventListener("DOMContentLoaded", () => {
      
      // Calculate Browser Entropy
      const nav = window.navigator;
      const entropyStr = `${nav.userAgent}|${nav.language}|${nav.hardwareConcurrency}|${nav.deviceMemory}|${screen.width}x${screen.height}|${screen.colorDepth}`;
      let hash = 0;
      for (let i = 0; i < entropyStr.length; i++) {
          hash = ((hash << 5) - hash) + entropyStr.charCodeAt(i);
          hash |= 0; 
      }
      this.telemetry.browserEntropy = Math.abs(hash);
      
      // Now it's safe to update the UI
      document.getElementById("hud-entropy").innerText = this.telemetry.browserEntropy;
      document.getElementById("ui-entropy").innerText = this.telemetry.browserEntropy;

      // 2. Track Typing Rhythm
      const inputs = document.querySelectorAll(".auth-input");
      inputs.forEach(input => {
        input.addEventListener("keydown", (e) => {
          let now = performance.now();
          if (this.telemetry.lastKeyTime !== 0 && e.key.length === 1) { 
            let flightTime = now - this.telemetry.lastKeyTime;
            if (flightTime < 1000) { 
                this.telemetry.keyIntervals.push(flightTime);
                let sum = this.telemetry.keyIntervals.reduce((a, b) => a + b, 0);
                this.telemetry.typingRhythm = sum / this.telemetry.keyIntervals.length;
                
                document.getElementById("hud-typing").innerText = Math.round(this.telemetry.typingRhythm);
                document.getElementById("ui-typing").innerText = Math.round(this.telemetry.typingRhythm) + " ms";
            }
          }
          this.telemetry.lastKeyTime = now;
        });
      });
      
      this.attachToScraperTraps();
    });

    // 3. Passive Signal Listener
    window.addEventListener("resize", () => {
      this.telemetry.resizeEvents++;
    });

    // 4. Mouse Tracking
    document.addEventListener("mousemove", (e) => {
      this.telemetry.mouseMovements++;

      let now = performance.now();
      if (this.telemetry.lastMouseTime !== 0) {
        let delta = now - this.telemetry.lastMouseTime;
        if (delta < 100) { 
          this.telemetry.mouseIntervals.push(delta);
          if (this.telemetry.mouseIntervals.length > 50) this.telemetry.mouseIntervals.shift();
          let sum = this.telemetry.mouseIntervals.reduce((a, b) => a + b, 0);
          this.telemetry.pollingRate = sum / this.telemetry.mouseIntervals.length;
        }
      }
      this.telemetry.lastMouseTime = now;

      if (this.telemetry.lastCoords) {
        const dx = e.clientX - this.telemetry.lastCoords.x;
        const dy = e.clientY - this.telemetry.lastCoords.y;
        const angle = Math.atan2(dy, dx);
        this.movementLog.push(angle);
        if (this.movementLog.length > 10) {
          this.movementLog.shift();
          const isLinear = this.movementLog.every((a) => a === this.movementLog[0]);
          if (isLinear) this.telemetry.linearityScore++;
        }
      }
      this.telemetry.lastCoords = { x: e.clientX, y: e.clientY };

      // Safely update HUD and Sidebar
      const hudX = document.getElementById("hud-x");
      if (hudX) {
        hudX.innerText = e.clientX;
        document.getElementById("hud-y").innerText = e.clientY;
        document.getElementById("hud-polling").innerText = this.telemetry.pollingRate.toFixed(1);
        
        // This makes the sidebar "Mouse Events" number tick up actively!
        const uiMouse = document.getElementById("ui-mouse");
        if (uiMouse) uiMouse.innerText = this.telemetry.mouseMovements;
      }
    });
  },

  attachToScraperTraps: function () {
    const buttons = document.querySelectorAll(".trap-btn");
    buttons.forEach((btn) => {
      btn.addEventListener("click", async () => {
        this.telemetry.requestTiming = Math.round(performance.now() - this.startTime);
        
        const reqUi = document.getElementById("ui-req-time");
        if (reqUi) reqUi.innerText = this.telemetry.requestTiming + " ms";

        const statusText = document.getElementById("status-text");
        const statusDisplay = document.getElementById("status-display");
        
        statusText.innerText = "Analyzing Telemetry...";
        statusText.style.color = "#38bdf8";
        
        try {
          let response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                mouseMovements: this.telemetry.mouseMovements,
                scrollDepth: 0, 
                timeOnPage: Math.floor(this.telemetry.requestTiming / 1000),
                linearityScore: this.telemetry.linearityScore,
                resizeEvents: this.telemetry.resizeEvents,
                pollingRate: this.telemetry.pollingRate,
                typingRhythm: this.telemetry.typingRhythm,
                browserEntropy: this.telemetry.browserEntropy,
                requestTiming: this.telemetry.requestTiming
            }),
          });
          
          if (!response.ok) throw new Error("Backend connection failed");
          let result = await response.json();
          
          if (result.is_bot) {
            statusText.innerText = "🚨 FRAUD BLOCKED 🚨";
            statusText.style.color = "#ef4444";
            statusDisplay.style.borderColor = "#ef4444";
            btn.disabled = true;
            
            // Deploy Active Defense Trap
            if (typeof CounterStrike !== 'undefined') {
                CounterStrike.deployTrap();
            }
          } else if (result.is_good_bot) {
            statusText.innerText = "🤖 GOOD BOT VERIFIED";
            statusText.style.color = "#22c55e";
            statusDisplay.style.borderColor = "#22c55e";
          } else {
            statusText.innerText = "✅ TRANSACTION APPROVED";
            statusText.style.color = "#22c55e";
            statusDisplay.style.borderColor = "#22c55e";
          }
        } catch (e) {
          console.error("Telemetry Error:", e);
          statusText.innerText = "❌ CONNECTION ERROR";
          statusText.style.color = "#ef4444";
        }
      });
    });
  }
};
ThreatShield.init();