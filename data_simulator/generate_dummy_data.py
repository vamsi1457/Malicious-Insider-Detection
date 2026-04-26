import csv
import random
from datetime import datetime, timedelta
import os

def generate_logs():
    num_logs = 200
    
    # Save it exactly in the simulator folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(base_dir, "mock_logs.csv")

    users = [f"EMP_{i:03d}" for i in range(1, 11)]
    normal_ips = ["192.168.1.10", "192.168.1.15", "10.0.0.5"]
    normal_actions = ["login", "view_dashboard", "edit_profile", "logout"]

    start_time = datetime.now() - timedelta(hours=2)

    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "user_id", "ip_address", "action", "status"])

        for _ in range(num_logs):
            current_time = start_time + timedelta(minutes=random.randint(1, 5))
            start_time = current_time

            # 5% chance of being a threat
            is_malicious = random.random() < 0.05

            user = random.choice(users)
            ip = random.choice(normal_ips)

            if not is_malicious:
                action = random.choice(normal_actions)
                status = "success"
            else:
                # Idi mana API engine catch chese threat!
                action = "download_entire_database" 
                status = "success"

            writer.writerow([current_time.strftime("%Y-%m-%d %H:%M:%S"), user, ip, action, status])

    print(f"✅ Created {num_logs} dummy logs in mock_logs.csv")

if __name__ == "__main__":
    generate_logs()