from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import warnings

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
    canvasHash: int = 0            
    audioHash: int = 0             
    hardwareMismatch: bool = False # NEW: Spoof Check

X_dummy = [
    [100, 15, 0, 1, 4.5, 200, 123456, 15000, 12345678, 55555555], 
    [5, 1, 10, 0, 16.0, 0, 111111, 1000, 999999999, 888888888]    
]
y_dummy = [0, 1] 

ml_model = RandomForestClassifier(n_estimators=10, random_state=42)
ml_model.fit(X_dummy, y_dummy)
print("✅ ThreatShield Multimodal ML Engine Online!")

@app.post("/analyze")
async def analyze(data: Telemetry, request: Request):
    user_agent = request.headers.get("user-agent", "")
    
    if "Googlebot" in user_agent:
        db["total"] += 1
        db["humans"] += 1 
        entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "is_bot": False, 
            "confidence": 100,
            "reason": "Verified Good Bot (Googlebot)",
            "typingRhythm": data.typingRhythm,
            "browserEntropy": data.browserEntropy,
            "requestTiming": data.requestTiming,
            "canvasHash": data.canvasHash,
            "audioHash": data.audioHash,
            "hardwareMismatch": data.hardwareMismatch
        }
        db["history"].append(entry)
        return {"is_bot": False, "is_good_bot": True}

    KNOWN_HEADLESS_CANVAS = 999999999 
    KNOWN_DUMMY_AUDIO = 888888888
    
    # Check for any fatal anomaly traps
    fatal_reasons = []
    if data.canvasHash == KNOWN_HEADLESS_CANVAS:
        fatal_reasons.append("GPU Canvas Emulation")
    if data.audioHash == KNOWN_DUMMY_AUDIO:
        fatal_reasons.append("Dummy Audio DAC")
    if data.hardwareMismatch:
        fatal_reasons.append("Mobile UA Spoofing")
        
    if fatal_reasons:
        is_bot = True
        ml_confidence = 100.0
        final_reason = "FATAL: " + " | ".join(fatal_reasons)
        print(f"🚨 ANOMALY: {final_reason}")
    else:
        # Standard ML Fraud Detection 
        features = [[
            data.mouseMovements, data.timeOnPage, data.linearityScore, 
            data.resizeEvents, data.pollingRate, data.typingRhythm, 
            data.browserEntropy, data.requestTiming, data.canvasHash, data.audioHash
        ]]
        
        prediction = ml_model.predict(features)[0]
        probabilities = ml_model.predict_proba(features)[0]
        
        is_bot = bool(prediction == 1)
        ml_confidence = round(max(probabilities) * 100, 2)
        final_reason = f"ML Classification (RF Model)"

    db["total"] += 1
    db["bots" if is_bot else "humans"] += 1
    
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "is_bot": is_bot,
        "confidence": ml_confidence,
        "reason": final_reason,
        "typingRhythm": data.typingRhythm,
        "browserEntropy": data.browserEntropy,
        "requestTiming": data.requestTiming,
        "canvasHash": data.canvasHash,
        "audioHash": data.audioHash,
        "hardwareMismatch": data.hardwareMismatch
    }
    db["history"].append(entry)
    
    return {"is_bot": is_bot, "is_good_bot": False}

@app.get("/stats")
async def get_stats():
    return db