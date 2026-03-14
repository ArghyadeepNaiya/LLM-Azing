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
    isTrustedEvent: bool  # Hardware verification
    canvasHash: str       # GPU hash
    memoryLeaks: bool     # Selenium artifacts

@app.post("/analyze")
async def analyze(data: Telemetry):
    human_score = 100
    reasons = []

    # 1. HARDWARE VERIFICATION (The Ultimate Check)
    # If a script triggered the click, it's an instant fail.
    if data.isTrustedEvent == False:
        human_score -= 100
        reasons.append("DOM Injection (Non-Physical Click)")

    # 2. MEMORY LEAK CHECK
    if data.memoryLeaks:
        human_score -= 80
        reasons.append("Automation Framework Detected in Memory")

    # 3. KINEMATICS & ACTIVITY
    if data.mouseMovements < 5:
        human_score -= 40
        reasons.append("Zero Physical Kinematics")

    is_bot = human_score < 50
    final_reason = ", ".join(reasons) if reasons else "Trusted Hardware & Kinematics"

    db["total"] += 1
    if is_bot:
        db["bots"] += 1
    else:
        db["humans"] += 1
    
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "is_bot": is_bot,
        "confidence": 100 - human_score if is_bot else human_score,
        "reason": final_reason
    }
    db["history"].append(entry)
    
    print(f"🛡️ Threat Analysis | Score: {human_score} | Flagged: {final_reason}")
    return {"is_bot": is_bot}

@app.get("/stats")
async def get_stats():
    return db