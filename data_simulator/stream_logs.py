import csv
import time
import requests
import os

def stream_logs():
    api_url = "http://127.0.0.1:8000/api/v1/ingest_log"
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, "mock_logs.csv")
    
    if not os.path.exists(csv_file):
        print("❌ mock_logs.csv not found! Run generate_dummy_data.py first.")
        return

    print("🚀 Starting live log stream to API... (Press CTRL+C to stop)")
    
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            payload = {
                "timestamp": row['timestamp'],
                "user_id": row['user_id'],
                "ip_address": row['ip_address'],
                "action": row['action'],
                "status": row['status']
            }
            
            try:
                response = requests.post(api_url, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("is_threat"):
                        print(f"⚠️ Sent log for {row['user_id']} -> API flagged as THREAT! Saved to DB.")
                    else:
                        print(f"✅ Sent log for {row['user_id']} -> Normal. Saved to DB.")
                else:
                    print(f"❌ API Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                print("❌ Cannot connect to API. Is the server running?")
                break
                
            time.sleep(2) # 2 seconds wait for realistic stream

if __name__ == "__main__":
    stream_logs()