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
    canvasHash: 0,     
    audioHash: 0,      
    hardwareMismatch: false, 
    forceChallenge: false, 
    authClickCount: 0, // NEW: Tracks rapid clicks on the authorize button
    
    lastCoords: null,
    lastMouseTime: 0,
    mouseIntervals: [],
    keyIntervals: [],
    lastKeyTime: 0
  },

  movementLog: [],
  startTime: performance.now(),

  generateCanvasHash: function() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx.textBaseline = "top";
    ctx.font = "14px 'Arial'";
    ctx.textBaseline = "alphabetic";
    ctx.fillStyle = "#f60";
    ctx.fillRect(125, 1, 62, 20);
    ctx.fillStyle = "#069";
    ctx.fillText("ThreatShield", 2, 15);
    ctx.fillStyle = "rgba(102, 204, 0, 0.7)";
    ctx.fillText("ThreatShield", 4, 17);
    
    const dataURI = canvas.toDataURL();
    let hash = 0;
    for (let i = 0; i < dataURI.length; i++) {
        hash = ((hash << 5) - hash) + dataURI.charCodeAt(i);
        hash |= 0; 
    }
    return Math.abs(hash);
  },

  generateAudioHash: async function() {
    try {
        const AudioContext = window.OfflineAudioContext || window.webkitOfflineAudioContext;
        const context = new AudioContext(1, 44100, 44100);
        const oscillator = context.createOscillator();
        oscillator.type = "triangle";
        oscillator.frequency.value = 10000;
        
        const compressor = context.createDynamicsCompressor();
        compressor.threshold.value = -50;
        compressor.knee.value = 40;
        compressor.ratio.value = 12;
        compressor.attack.value = 0;
        compressor.release.value = 0.25;

        oscillator.connect(compressor);
        compressor.connect(context.destination);
        oscillator.start(0);

        const buffer = await context.startRendering();
        const data = buffer.getChannelData(0);
        let hash = 0;
        for (let i = 4500; i < 5000; i++) {
            hash += Math.abs(data[i]);
        }
        return Math.floor(hash * 10000000);
    } catch (e) {
        return 0; 
    }
  },

  init: function () {
    // Session Storage tracking for the "Uncertainty" trigger (4 reloads)
    let reloads = parseInt(sessionStorage.getItem('threatshield_reloads') || '0');
    reloads++;
    sessionStorage.setItem('threatshield_reloads', reloads.toString());
    
    if (reloads >= 4) {
        this.telemetry.forceChallenge = true;
    }

    document.addEventListener("DOMContentLoaded", async () => {
      
      const ua = navigator.userAgent.toLowerCase();
      const isMobile = /iphone|ipad|android|mobile/.test(ua);
      const cores = navigator.hardwareConcurrency || 4;
      const memory = navigator.deviceMemory || 4;
      this.telemetry.hardwareMismatch = isMobile && (cores > 8 || memory > 8);
      
      this.telemetry.canvasHash = this.generateCanvasHash();
      this.telemetry.audioHash = await this.generateAudioHash(); 
      
      const nav = window.navigator;
      const entropyStr = `${nav.userAgent}|${nav.language}|${nav.hardwareConcurrency}|${nav.deviceMemory}|${screen.width}x${screen.height}|${screen.colorDepth}`;
      let hash = 0;
      for (let i = 0; i < entropyStr.length; i++) {
          hash = ((hash << 5) - hash) + entropyStr.charCodeAt(i);
          hash |= 0; 
      }
      this.telemetry.browserEntropy = Math.abs(hash);
      
      const hudEntropy = document.getElementById("hud-entropy");
      const uiEntropy = document.getElementById("ui-entropy");
      if(hudEntropy) hudEntropy.innerText = this.telemetry.browserEntropy;
      if(uiEntropy) uiEntropy.innerText = this.telemetry.browserEntropy;

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

    window.addEventListener("resize", () => {
      this.telemetry.resizeEvents++;
    });

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

      const hudX = document.getElementById("hud-x");
      if (hudX) {
        hudX.innerText = e.clientX;
        document.getElementById("hud-y").innerText = e.clientY;
        document.getElementById("hud-polling").innerText = this.telemetry.pollingRate.toFixed(1);
        
        const uiMouse = document.getElementById("ui-mouse");
        if (uiMouse) uiMouse.innerText = this.telemetry.mouseMovements;
      }
    });
  },

  attachToScraperTraps: function () {
    const buttons = document.querySelectorAll(".trap-btn");
    buttons.forEach((btn) => {
      btn.addEventListener("click", async () => {
        
        // NEW: Increment the click counter. If they mash the button 4+ times, trigger the trap!
        this.telemetry.authClickCount++;
        if (this.telemetry.authClickCount >= 4) {
            this.telemetry.forceChallenge = true;
        }

        // ==========================================
        // THE "ML UNCERTAINTY" TRAP INTERCEPT
        // ==========================================
        if (this.telemetry.forceChallenge) {
            const statusText = document.getElementById("status-text");
            const statusDisplay = document.getElementById("status-display");
            
            // 1. Alert the UI that the ML is struggling
            statusText.innerText = "🟡 ML CONFIDENCE: 48% (UNCERTAIN)";
            statusText.style.color = "#fbbf24";
            statusDisplay.style.borderColor = "#fbbf24";
            
            // 2. Hide the button and show the slider challenge
            btn.style.display = "none";
            document.getElementById("active-challenge").style.display = "block";
            
            // 3. Listen for the slider to reach 100
            const slider = document.getElementById("kinematic-slider");
            slider.addEventListener("input", (e) => {
                if (e.target.value == 100) {
                    // Challenge Passed! Reset everything.
                    this.telemetry.forceChallenge = false;
                    this.telemetry.authClickCount = 0; // Reset the rapid-click counter
                    sessionStorage.setItem('threatshield_reloads', '0'); // Reset reload counter
                    
                    document.getElementById("active-challenge").style.display = "none";
                    btn.style.display = "block";
                    
                    statusText.innerText = "✅ Kinematics verified. Finalizing...";
                    statusText.style.color = "#22c55e";
                    statusDisplay.style.borderColor = "#22c55e";
                    
                    // Programmatically click the button again to continue the normal auth flow
                    setTimeout(() => { btn.click(); }, 500); 
                }
            });
            return; // STOP execution here until they finish the slider!
        }
        // ==========================================

        this.telemetry.requestTiming = Math.round(performance.now() - this.startTime);
        
        const reqUi = document.getElementById("ui-req-time");
        if (reqUi) reqUi.innerText = this.telemetry.requestTiming + " ms";

        const statusText = document.getElementById("status-text");
        const statusDisplay = document.getElementById("status-display");
        
        if(statusText) {
            statusText.innerText = "Analyzing Telemetry...";
            statusText.style.color = "#38bdf8";
        }
        
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
                requestTiming: this.telemetry.requestTiming,
                canvasHash: this.telemetry.canvasHash,
                audioHash: this.telemetry.audioHash,
                hardwareMismatch: this.telemetry.hardwareMismatch 
            }),
          });
          
          if (!response.ok) throw new Error("Backend connection failed");
          let result = await response.json();
          
          if (result.is_bot) {
            if(statusText) {
                statusText.innerText = "🚨 FRAUD BLOCKED 🚨";
                statusText.style.color = "#ef4444";
                statusDisplay.style.borderColor = "#ef4444";
            }
            btn.disabled = true;
            
            if (typeof CounterStrike !== 'undefined') {
                CounterStrike.deployTrap();
            }
          } else if (result.is_good_bot) {
            if(statusText) {
                statusText.innerText = "🤖 GOOD BOT VERIFIED";
                statusText.style.color = "#22c55e";
                statusDisplay.style.borderColor = "#22c55e";
            }
          } else {
            if(statusText) {
                statusText.innerText = "✅ TRANSACTION APPROVED";
                statusText.style.color = "#22c55e";
                statusDisplay.style.borderColor = "#22c55e";
            }
          }
        } catch (e) {
          console.error("Telemetry Error:", e);
          if(statusText) {
              statusText.innerText = "❌ CONNECTION ERROR";
              statusText.style.color = "#ef4444";
          }
        }
      });
    });
  }
};
ThreatShield.init();