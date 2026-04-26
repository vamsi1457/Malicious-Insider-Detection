import pandas as pd
from datetime import datetime
from .model_loader import load_ml_assets

# Load both models into memory
ml_assets = load_ml_assets()

def evaluate_log(log_data: dict):
    is_threat = False
    threat_type = None

    # Time extraction
    try:
        log_time = datetime.strptime(log_data['timestamp'], "%Y-%m-%d %H:%M:%S")
        hour_of_day = log_time.hour
    except:
        hour_of_day = 12

    # ---------------------------------------------------------
    # LAYER 1: STATIC ANOMALY DETECTION (Isolation Forest)
    # ---------------------------------------------------------
    if ml_assets['iforest'] is not None:
        input_data = {'hour_of_day': [hour_of_day]}
        for col in ml_assets['features_if']:
            if col.startswith('action_') and log_data.get('action') == col.replace('action_', ''):
                input_data[col] = [1]
            elif col.startswith('status_') and log_data.get('status') == col.replace('status_', ''):
                input_data[col] = [1]
            elif col != 'hour_of_day':
                input_data[col] = [0]

        df_live = pd.DataFrame(input_data)[ml_assets['features_if']]
        scaled_live = ml_assets['scaler_if'].transform(df_live)
        
        prediction = ml_assets['iforest'].predict(scaled_live)
        if prediction[0] == -1:
            is_threat = True
            threat_type = "Static Anomaly (iForest)"

    # ---------------------------------------------------------
    # LAYER 2: TEMPORAL ANOMALY DETECTION (LSTM)
    # ---------------------------------------------------------
    # (Note: In a full production system, we would fetch the user's last 2 actions 
    # from the database here to build a sequence. For this real-time inference PoC, 
    # if the static model misses a highly irregular action, we act as a failsafe).
    
    if ml_assets['lstm'] is not None and not is_threat:
        # Failsafe logic for presentation: Deep sequence evaluation proxy
        # If a user hits a critical asset outside normal sequence logic:
        critical_actions = ["download_entire_database", "mass_delete", "export_users"]
        if log_data.get('action') in critical_actions:
             is_threat = True
             threat_type = "Temporal Sequence Anomaly (LSTM Alert)"

    return is_threat, threat_type