import threading
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import warnings

# Hide scikit-learn warnings to keep your terminal clean
warnings.filterwarnings("ignore") 

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

db = {"total": 0, "humans": 0, "bots": 0, "history": []}

class Telemetry(BaseModel):
    mouseMovements: int
    scrollDepth: int
    timeOnPage: int
    linearityScore: int
    resizeEvents: int = 0
    pollingRate: float = 0.0
    typingRhythm: float = 0.0      
    browserEntropy: int = 0        
    requestTiming: int = 0         

# ==========================================
# 🧠 ML SETUP (DUMMY TRAINING)
# ==========================================
X_dummy = [
    [100, 15, 0, 1, 4.5, 200, 123456, 15000], # Human profile
    [5, 1, 10, 0, 16.0, 0, 111111, 1000]      # Bot profile
]
y_dummy = [0, 1] # 0 = Human, 1 = Bot

ml_model = RandomForestClassifier(n_estimators=10, random_state=42)
ml_model.fit(X_dummy, y_dummy)

# ==========================================
# 🎮 TERMINAL OVERRIDE (BACKGROUND THREAD)
# ==========================================
# This variable controls the server behavior instantly
SYSTEM_MODE = "auto" 

def terminal_listener():
    global SYSTEM_MODE
    print("\n" + "="*50)
    print("🛡️ THREATSHIELD TERMINAL OVERRIDE ACTIVE")
    print(" -> Type 'legal' to force ALLOW all traffic.")
    print(" -> Type 'illegal' to force BLOCK all traffic.")
    print(" -> Type 'auto' to let the ML model decide.")
    print("="*50 + "\n")
    
    while True:
        try:
            cmd = input().strip().lower()
            if cmd in ['legal', 'illegal', 'auto']:
                SYSTEM_MODE = cmd
                print(f"\n👉 [SYSTEM MODE CHANGED TO: {cmd.upper()}]\n")
            elif cmd:
                print("❌ Invalid command. Type 'legal', 'illegal', or 'auto'.")
        except EOFError:
            break
        except Exception:
            pass

# Start the keyboard listener in the background immediately
listener_thread = threading.Thread(target=terminal_listener, daemon=True)
listener_thread.start()
# ==========================================

@app.post("/analyze")
async def analyze(data: Telemetry, request: Request):
    global SYSTEM_MODE
    
    # 1. Prepare ML Features
    features = [[
        data.mouseMovements, data.timeOnPage, data.linearityScore, 
        data.resizeEvents, data.pollingRate, data.typingRhythm, 
        data.browserEntropy, data.requestTiming
    ]]
    
    # 2. Get ML Prediction (Runs in milliseconds)
    prediction = ml_model.predict(features)[0]
    probabilities = ml_model.predict_proba(features)[0]
    ml_confidence = round(max(probabilities) * 100, 2)
    ml_is_bot = bool(prediction == 1)
    
    # 3. Check Manual Override (No waiting!)
    is_good_bot = False
    
    if SYSTEM_MODE == 'legal':
        is_bot = False
        is_good_bot = True # Flags green on the UI
        final_reason = "Manual Override: LEGAL (Allowed)"
        final_confidence = 100.0
        print("\n✅ Incoming request ALLOWED by terminal override.")
        
    elif SYSTEM_MODE == 'illegal':
        is_bot = True
        final_reason = "Manual Override: ILLEGAL (Blocked)"
        final_confidence = 100.0
        print("\n🛑 Incoming request BLOCKED by terminal override.")
        
    else: # "auto" mode
        is_bot = ml_is_bot
        final_reason = f"ML Classification (RF Model)"
        final_confidence = ml_confidence
        print(f"\n⚙️ Incoming request processed by ML: {'BOT' if is_bot else 'HUMAN'} ({ml_confidence}% conf)")

    # 4. Save to Database for Admin UI
    db["total"] += 1
    db["bots" if is_bot else "humans"] += 1
    
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "is_bot": is_bot,
        "confidence": final_confidence,
        "reason": final_reason,
        "typingRhythm": data.typingRhythm,
        "browserEntropy": data.browserEntropy,
        "requestTiming": data.requestTiming
    }
    db["history"].append(entry)
    
    return {"is_bot": is_bot, "is_good_bot": is_good_bot}

@app.get("/stats")
async def get_stats():
    return db