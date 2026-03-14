from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestClassifier

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- MACHINE LEARNING ENGINE ---
print("🧠 Training ThreatShield ML Model...")
# Features: [mouse_movements, scroll_depth, time_on_page, linearity, has_valid_asn]
# Labels: 0 = Bad Bot (Illegal), 1 = Human, 2 = Good Bot (Legal)
X_train = np.array([
    # HUMANS (High movement, moderate scroll, varied time, low linearity, no ASN)
    [150, 800, 15, 0, 0], 
    [85, 400, 8, 1, 0], 
    [200, 1200, 45, 0, 0], 
    [45, 100, 5, 1, 0],
    [15, 0, 2, 0, 0],   # NEW: Fast Human (Tested the page quickly, low linearity)
    [25, 50, 3, 1, 0],  # NEW: Another fast human profile
    
    # BAD BOTS (Low/Linear movement, teleportation, fast time, no verified ASN)
    [5, 0, 1, 5, 0], 
    [12, 50, 2, 8, 0], 
    [0, 0, 0, 0, 0], 
    [25, 600, 1, 8, 0], # High linearity reveals it's a bot despite movements
    [10, 0, 0, 9, 0],   # NEW: Fast, highly linear bot
    
    # GOOD BOTS (Zero/Low movement, zero scroll, fast time, BUT has a Verified ASN/FCrDNS)
    [0, 0, 1, 0, 1], 
    [2, 0, 2, 0, 1], 
    [0, 50, 1, 0, 1], 
    [0, 0, 0, 0, 1],
    [5, 0, 0, 0, 1]     # NEW: Extra Good Bot baseline
])

# Labels perfectly matched to the arrays above
y_train = np.array([1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2])

# Train a Random Forest to find non-linear patterns in the data
ml_model = RandomForestClassifier(n_estimators=50, random_state=42)
ml_model.fit(X_train, y_train)
print("✅ ML Model Ready.")

# --- IN-MEMORY DATABASE ---
db = {"total": 0, "humans": 0, "bad_bots": 0, "good_bots": 0, "history": []}

class Telemetry(BaseModel):
    mouseMovements: int
    scrollDepth: int
    timeOnPage: int
    linearityScore: int = 0

@app.post("/analyze")
async def analyze(data: Telemetry, request: Request):
    # 1. Simulate ASN / FCrDNS Check
    # FastAPI forces header keys to lowercase. Check for it safely.
    header_value = request.headers.get("x-verified-asn", "").upper()
    has_valid_asn = 1 if header_value == "TRUE" else 0

    # 2. Prepare data for the ML Model
    features = np.array([[
        data.mouseMovements, 
        data.scrollDepth, 
        data.timeOnPage, 
        data.linearityScore, 
        has_valid_asn
    ]])

    # 3. Ask the ML Model for a prediction
    prediction = ml_model.predict(features)[0]
    probabilities = ml_model.predict_proba(features)[0]
    confidence = round(max(probabilities) * 100, 1)

    # 4. Interpret Results
    if prediction == 1:
        category = "Human"
        is_bot = False
        db["humans"] += 1
        reason = "Passed Biometrics"
    elif prediction == 2:
        category = "Good Bot"
        is_bot = False # We allow it through
        db["good_bots"] += 1
        reason = "Verified ASN/FCrDNS"
    else:
        category = "Bad Bot"
        is_bot = True # Blocked!
        db["bad_bots"] += 1
        reason = "Failed ML Kinematics & DNS"

    db["total"] += 1
    
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "is_bot": is_bot,
        "category": category,
        "confidence": confidence,
        "reason": reason
    }
    db["history"].append(entry)
    
    print(f"📊 ML Prediction: {category} ({confidence}%) | ASN Valid: {bool(has_valid_asn)}")
    
    return {"is_bot": is_bot, "category": category}

@app.get("/stats")
async def get_stats():
    return {
        "total": db["total"],
        "humans": db["humans"] + db["good_bots"], 
        "bots": db["bad_bots"],
        "history": db["history"]
    }