import os
import joblib

def load_ml_assets():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = os.path.join(current_dir, '..', '..', 'ml_training', 'artifacts')
    
    models = {
        'iforest': None, 'scaler_if': None, 'features_if': None,
        'lstm': None, 'scaler_lstm': None, 'features_lstm': None
    }
    
    # 1. Load Static Model (Isolation Forest)
    try:
        models['iforest'] = joblib.load(os.path.join(artifacts_dir, 'isolation_forest.pkl'))
        models['scaler_if'] = joblib.load(os.path.join(artifacts_dir, 'scaler.pkl'))
        models['features_if'] = joblib.load(os.path.join(artifacts_dir, 'feature_columns.pkl'))
        print("✅ Static Model (iForest) Loaded.")
    except:
        print("⚠️ Static Model not found.")

    # 2. Load Temporal Model (LSTM)
    try:
        from tensorflow.keras.models import load_model # type: ignore
        models['lstm'] = load_model(os.path.join(artifacts_dir, 'lstm_model.h5'))
        models['scaler_lstm'] = joblib.load(os.path.join(artifacts_dir, 'scaler_lstm.pkl'))
        models['features_lstm'] = joblib.load(os.path.join(artifacts_dir, 'feature_columns_lstm.pkl'))
        print("✅ Temporal Model (LSTM) Loaded.")
    except Exception as e:
        print(f"⚠️ Temporal Model not found or error: {e}")

    return models