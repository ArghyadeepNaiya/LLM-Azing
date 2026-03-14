from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

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
    typingRhythm: float = 0.0      # NEW: Keystroke dynamics
    browserEntropy: int = 0        # NEW: Hardware/Software fingerprint
    requestTiming: int = 0         # NEW: Total ms to click

@app.post("/analyze")
async def analyze(data: Telemetry, request: Request):
    user_agent = request.headers.get("user-agent", "")
    
    # --- 1. GOOD BOT CHECK ---
    if "Googlebot" in user_agent:
        db["total"] += 1
        db["humans"] += 1 # Counting legal bots as valid traffic
        entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "is_bot": False, 
            "confidence": 100,
            "reason": "Verified Good Bot (Googlebot)",
            "typingRhythm": data.typingRhythm,
            "browserEntropy": data.browserEntropy,
            "requestTiming": data.requestTiming
        }
        db["history"].append(entry)
        return {"is_bot": False, "is_good_bot": True}

    # --- 2. BAD BOT HEURISTICS ---
    human_score = 100
    reasons = []

    # Kinematics & Timing
    if data.linearityScore > 2:
        human_score -= 70
        reasons.append("Non-human Kinematics (Linear)")

    if data.timeOnPage < 3:
        human_score -= 40
        reasons.append("Rapid Interaction")

    # Mouse Teleportation / Jitter
    if data.mouseMovements < 10:
        human_score -= 60
        reasons.append("Mouse Teleportation")
    elif data.mouseMovements < 40:
        human_score -= 30
        reasons.append("Insufficient Jitter")

    # Passive Signal Check (Window Resizing)
    if data.resizeEvents > 4:
        human_score -= 50
        reasons.append("Unnatural Passive Signaling")

    # Hardware Polling Rate Check
    # Only analyze if we have enough data points to get a real average
    if data.mouseMovements > 20:
        if data.pollingRate > 12.0:
            human_score -= 40
            reasons.append(f"Software Polling Rate ({data.pollingRate:.1f}ms)")
        elif data.pollingRate > 0 and data.pollingRate < 8.0:
            human_score += 10  # Bonus for verifiable hardware speeds

    # Final scoring evaluation
    is_bot = human_score < 50
    final_reason = ", ".join(reasons) if reasons else "Natural Movement"

    db["total"] += 1
    db["bots" if is_bot else "humans"] += 1
    
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "is_bot": is_bot,
        # Ensure confidence visually stays between 0 and 100 for the UI
        "confidence": max(0, 100 - human_score) if is_bot else min(100, human_score),
        "reason": final_reason,
        "typingRhythm": data.typingRhythm,
        "browserEntropy": data.browserEntropy,
        "requestTiming": data.requestTiming
    }
    db["history"].append(entry)
    
    return {"is_bot": is_bot, "is_good_bot": False}

@app.get("/stats")
async def get_stats():
    return db