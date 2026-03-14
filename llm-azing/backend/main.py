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

@app.post("/analyze")
async def analyze(data: Telemetry, request: Request):
    # --- 1. GOOD BOT CHECK (Bypass Heuristics) ---
    # Look for the header injected by legal crawlers/anti-piracy bots
    is_good_bot = request.headers.get("x-verified-asn") == "TRUE"
    
    if is_good_bot:
        db["total"] += 1
        db["humans"] += 1 # Counting as valid traffic
        entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "is_bot": False, 
            "confidence": 100,
            "reason": "Verified Good Bot (ASN/Google)"
        }
        db["history"].append(entry)
        # Return a custom flag so the frontend knows it's a friendly bot
        return {"is_bot": False, "is_good_bot": True}

    # --- 2. BAD BOT HEURISTICS ---
    human_score = 100
    reasons = []

    if data.linearityScore > 2:
        human_score -= 70
        reasons.append("Non-human Kinematics (Linear)")

    if data.timeOnPage < 3:
        human_score -= 40
        reasons.append("Rapid Interaction")

    # NEW: Detect Selenium/Puppeteer cursor teleportation
    if data.mouseMovements < 10:
        human_score -= 60  # Massive penalty for instant teleportation
        reasons.append("Mouse Teleportation")
    elif data.mouseMovements < 40:
        human_score -= 30
        reasons.append("Insufficient Jitter")

    is_bot = human_score < 50
    final_reason = ", ".join(reasons) if reasons else "Natural Curved Movements"

    db["total"] += 1
    db["bots" if is_bot else "humans"] += 1
    
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "is_bot": is_bot,
        "confidence": 100 - human_score if is_bot else human_score,
        "reason": final_reason
    }
    db["history"].append(entry)
    
    return {"is_bot": is_bot, "is_good_bot": False}

@app.get("/stats")
async def get_stats():
    return db