from sqlalchemy.orm import Session
from .config import SessionLocal, SystemLog, User
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- User/Auth Operations ---
def get_admin():
    db = SessionLocal()
    try:
        return db.query(User).filter(User.username == "admin").first()
    finally:
        db.close()

def create_admin(password: str):
    db = SessionLocal()
    try:
        new_user = User(username="admin", password=password)
        db.add(new_user)
        db.commit()
        return True
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        db.rollback()
        return False
    finally:
        db.close()

# --- Log Operations ---
def save_log_to_db(log_data: dict, is_threat: bool, threat_type: str = None):
    db = SessionLocal()
    try:
        log_time = datetime.strptime(log_data['timestamp'], "%Y-%m-%d %H:%M:%S")
        new_log = SystemLog(
            timestamp=log_time,
            user_id=log_data['user_id'],
            ip_address=log_data['ip_address'],
            action=log_data['action'],
            status=log_data['status'],
            is_threat=is_threat,
            threat_type=threat_type
        )
        db.add(new_log)
        db.commit()
        return True
    except Exception as e:
        print(f"❌ Database Save Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def get_recent_logs(limit: int = 100):
    db = SessionLocal()
    try:
        logs = db.query(SystemLog).order_by(SystemLog.timestamp.desc()).limit(limit).all()
        return logs
    finally:
        db.close()