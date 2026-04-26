import pandas as pd
import os
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def train_static_model():
    print("⏳ Starting Isolation Forest Training...")
    
    # 1. Path Setup
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data_simulator', 'mock_logs.csv')
    artifacts_dir = os.path.join(base_dir, 'artifacts')
    
    if not os.path.exists(data_path):
        print(f"❌ Error: Training data not found at {data_path}. Run simulator first.")
        return

    # 2. Load Data
    df = pd.read_csv(data_path)
    print(f"✅ Loaded {len(df)} historical logs.")

    # 3. Feature Engineering (The Brains)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour_of_day'] = df['timestamp'].dt.hour
    
    # Drop identifying columns, we only care about behavior
    df_features = df.drop(columns=['timestamp', 'user_id', 'ip_address'])
    
    # One-Hot Encoding (Convert text actions to numbers)
    df_features = pd.get_dummies(df_features)

    # 4. Scaling
    print("🔄 Standardizing features...")
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_features)

    # 5. Model Training
    print("🧠 Training Isolation Forest (Contamination=0.05)...")
    model = IsolationForest(contamination=0.05, random_state=42) 
    model.fit(scaled_data)

    # 6. Save Artifacts
    os.makedirs(artifacts_dir, exist_ok=True)
    joblib.dump(model, os.path.join(artifacts_dir, 'isolation_forest.pkl'))
    joblib.dump(scaler, os.path.join(artifacts_dir, 'scaler.pkl'))
    joblib.dump(df_features.columns.tolist(), os.path.join(artifacts_dir, 'feature_columns.pkl'))

    print("✅ Success! Static Anomaly Model (iForest) saved to artifacts folder.")

if __name__ == "__main__":
    train_static_model()