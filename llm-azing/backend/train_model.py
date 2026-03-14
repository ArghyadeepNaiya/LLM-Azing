import xgboost as xgb
import numpy as np
import random

print("⚙️ Generating synthetic training data...")

def generate_human():
    return [
        random.uniform(5.0, 30.0),    # time_since_last_request
        random.randint(2, 15),        # mouse_clicks
        random.uniform(500, 2500),    # mouse_distance
        random.uniform(20.0, 100.0),  # scroll_depth
        random.uniform(30.0, 80.0),   # typing_speed
        random.randint(0, 50),        # key_presses
        random.choice([1920, 1440]),  # window_width
        random.choice([1080, 900]),   # window_height
        random.uniform(60.0, 600.0),  # session_length
        random.randint(1, 5),         # pages_visited
        random.randint(100, 130),     # user_agent_length
        1,                            # accept_language_present
        1,                            # cookie_enabled
        -240,                         # timezone_offset
        random.randint(3, 10),        # plugins_count
        0,                            # touch_support
        0,                            # bot_keyword_in_ua
        random.randint(1, 4),         # ip_request_rate_1m
        random.randint(5, 20),        # ip_request_rate_10m
        0                             # failed_logins
    ]

def generate_bot():
    return [
        random.uniform(0.01, 1.0),    # time_since_last_request (Fast)
        0,                            # mouse_clicks (None)
        0.0,                          # mouse_distance (None)
        0.0,                          # scroll_depth
        0.0,                          # typing_speed
        0,                            # key_presses
        800,                          # window_width (Headless default)
        600,                          # window_height
        random.uniform(0.5, 5.0),     # session_length (Short)
        random.randint(20, 100),      # pages_visited (High)
        random.randint(30, 60),       # user_agent_length (Short/Non-standard)
        0,                            # accept_language_present
        0,                            # cookie_enabled
        0,                            # timezone_offset
        0,                            # plugins_count
        0,                            # touch_support
        random.choice([0, 1]),        # bot_keyword_in_ua
        random.randint(50, 200),      # ip_request_rate_1m (High)
        random.randint(300, 1000),    # ip_request_rate_10m
        random.choice([0, 5, 10])     # failed_logins
    ]

# Create 1000 Humans (Label 0) and 1000 Bots (Label 1)
X_data = []
y_labels = []

for _ in range(1000):
    X_data.append(generate_human())
    y_labels.append(0)  # 0 = Human

for _ in range(1000):
    X_data.append(generate_bot())
    y_labels.append(1)  # 1 = Bot

# Convert to NumPy arrays for XGBoost
X = np.array(X_data, dtype=np.float32)
y = np.array(y_labels, dtype=np.float32)

print("🧠 Training XGBoost model...")

# Create DMatrix
dtrain = xgb.DMatrix(X, label=y)

# Set up parameters for binary classification
params = {
    'objective': 'binary:logistic',
    'eval_metric': 'logloss',
    'max_depth': 4,
    'learning_rate': 0.1
}

# Train the model
model = xgb.train(params, dtrain, num_boost_round=50)

# Save the model
model_filename = "bot_model.json"
model.save_model(model_filename)

print(f"✅ Model successfully trained and saved as '{model_filename}'!")
print("You are ready to start the FastAPI server.")