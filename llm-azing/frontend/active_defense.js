// active_defense.js
const CounterStrike = {
  deployTrap: function() {
    // 1. Trigger the Visual "Attack" UI for the Judges
    this.showDefenseUI();
    
    // 2. Start the Proof of Work (CPU Burner)
    setTimeout(() => {
      this.executeProofOfWork();
    }, 1000);
  },

  showDefenseUI: function() {
    const overlay = document.createElement('div');
    overlay.id = "defense-overlay";
    overlay.innerHTML = `
      <div style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(15, 0, 0, 0.9); z-index: 10000; display: flex; flex-direction: column; justify-content: center; align-items: center; color: #ff4444; font-family: monospace;">
        <h1 style="font-size: 3rem; text-shadow: 0 0 20px #ff4444; animation: blink 1s infinite;">⚠️ ACTIVE DEFENSE ENGAGED ⚠️</h1>
        <div style="background: #000; padding: 20px; border: 1px solid #ff4444; width: 600px; height: 300px; overflow-y: auto; font-size: 14px;" id="terminal-out">
          > Intrusion detected.<br>
          > Deploying tarpit protocol...<br>
        </div>
      </div>
      <style>
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
      </style>
    `;
    document.body.appendChild(overlay);
  },

  logTerminal: function(msg) {
    const term = document.getElementById("terminal-out");
    if (term) {
      term.innerHTML += `> ${msg}<br>`;
      term.scrollTop = term.scrollHeight;
    }
  },

  executeProofOfWork: function() {
    this.logTerminal("<span style='color: #fbbf24'>Initiating CPU Burner (Math Challenge)...</span>");
    
    // A heavy, blocking synchronous loop to max out the bot's CPU thread
    let nonce = 0;
    const targetDifficulty = 9999999; // Adjust to make it burn longer
    const startTime = performance.now();

    // The bot's thread will freeze here while it calculates
    while (true) {
      let hashSim = (nonce * 2654435761) % Math.pow(2, 32);
      if (nonce > targetDifficulty) {
        break;
      }
      if (nonce % 1000000 === 0) {
          this.logTerminal(`Calculating... Hash Rate: ${nonce}H/s`);
      }
      nonce++;
    }

    const endTime = performance.now();
    this.logTerminal(`<span style='color: #22c55e'>Challenge complete. CPU Time Wasted: ${((endTime - startTime)/1000).toFixed(2)} seconds.</span>`);
    
    // 3. Deploy Data Poisoning
    setTimeout(() => {
      this.injectPoison();
    }, 1000);
  },

  injectPoison: function() {
    this.logTerminal("<span style='color: #a855f7'>Injecting Poisoned Data into DOM...</span>");
    
    // Wipe the real data and feed the scraper garbage
    const feed = document.querySelector('.feed');
    if (feed) {
        feed.innerHTML = '';
        for(let i=0; i<5; i++) {
            feed.innerHTML += `
              <div class="post glass-panel">
                <div class="post-content">
                  <h2 class="post-title" style="color:#a855f7">HONEYPOT DATA: FAKE_${Math.random().toString(36).substring(7)}</h2>
                  <p class="post-snippet">This is poisoned data designed to corrupt the attacker's database. Fake email: admin_${Math.random().toString(36).substring(7)}@internal.corp. Fake API Key: sk_live_${Math.random().toString(36).substring(2)}</p>
                </div>
              </div>
            `;
        }
    }
    this.logTerminal("<span style='color: #ef4444'>Target successfully compromised.</span>");
  }
};

// You can trigger this function from your existing sensor.js when `result.is_bot` is true!
// Example: if (result.is_bot) { CounterStrike.deployTrap(); }