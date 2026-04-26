import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore

# This function turns individual logs into "Sequences" for each user
def create_sequences(df, seq_length=3):
    sequences = []
    labels = []
    
    # We group by user to track their individual journey
    for user_id, group in df.groupby('user_id'):
        group_features = group.drop(columns=['timestamp', 'user_id', 'ip_address']).values
        
        if len(group_features) >= seq_length:
            for i in range(len(group_features) - seq_length):
                seq = group_features[i:(i + seq_length)]
                # Target is the next action in the sequence
                target = group_features[i + seq_length]
                sequences.append(seq)
                labels.append(target)
                
    return np.array(sequences), np.array(labels)

def train_temporal_model():
    print("⏳ Starting Deep Learning (LSTM) Training...")
    
    # 1. Path Setup
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'data_simulator', 'mock_logs.csv')
    artifacts_dir = os.path.join(base_dir, 'artifacts')
    
    if not os.path.exists(data_path):
        print(f"❌ Error: Data not found at {data_path}.")
        return

    # 2. Data Prep (Similar to iForest but tailored for sequences)
    df = pd.read_csv(data_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour_of_day'] = df['timestamp'].dt.hour
    
    # Needs to be sorted by time so the sequence makes sense
    df = df.sort_values(by=['user_id', 'timestamp'])
    
    df_features = df[['user_id', 'timestamp', 'ip_address', 'action', 'status', 'hour_of_day']].copy()
    df_encoded = pd.get_dummies(df_features, columns=['action', 'status'])
    
    # Scaling
    scaler_lstm = StandardScaler()
    # We scale only the numeric columns, leaving out the identifiers
    cols_to_scale = [c for c in df_encoded.columns if c not in ['timestamp', 'user_id', 'ip_address']]
    df_encoded[cols_to_scale] = scaler_lstm.fit_transform(df_encoded[cols_to_scale])

    # 3. Create Sequences (Looking at 3 actions at a time)
    seq_length = 3
    X, y = create_sequences(df_encoded, seq_length)
    
    if len(X) == 0:
         print("❌ Not enough data to create sequences. Generate more dummy data.")
         return

    print(f"✅ Generated {len(X)} user sequences for training.")

    # 4. Build the LSTM Neural Network
    model = Sequential()
    # Input shape is (Sequence Length, Number of Features)
    model.add(LSTM(32, activation='relu', input_shape=(X.shape[1], X.shape[2]), return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1])) # Predicting the next feature state
    
    model.compile(optimizer='adam', loss='mse')
    
    print("🧠 Training Neural Network...")
    # Training for 10 epochs. In a real scenario, this would be much higher.
    model.fit(X, y, epochs=10, batch_size=16, verbose=1)

    # 5. Save the Model
    os.makedirs(artifacts_dir, exist_ok=True)
    
    # TensorFlow saves differently than Scikit-Learn
    model.save(os.path.join(artifacts_dir, 'lstm_model.h5'))
    joblib.dump(scaler_lstm, os.path.join(artifacts_dir, 'scaler_lstm.pkl'))
    joblib.dump(cols_to_scale, os.path.join(artifacts_dir, 'feature_columns_lstm.pkl'))
    
    print("✅ Success! Temporal Sequence Model (LSTM) saved to artifacts.")

if __name__ == "__main__":
    train_temporal_model()