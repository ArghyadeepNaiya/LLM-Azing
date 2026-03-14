from fastapi import FastAPI
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
    linearityScore: int  # Captured by our new kinematic sensor

@app.post("/analyze")
async def analyze(data: Telemetry):
    human_score = 100
    reasons = []

    # 1. Kinematic Check: Straight lines are a bot signature
    if data.linearityScore > 2:
        human_score -= 70
        reasons.append("Non-human Kinematics (Linear)")

    # 2. Advanced Timing Check: Very consistent behavior
    if data.timeOnPage < 3:
        human_score -= 40
        reasons.append("Rapid Interaction")

    # 3. Movement Quantity
    if data.mouseMovements < 40:
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
    
    return {"is_bot": is_bot}

@app.get("/stats")
async def get_stats():
    return db