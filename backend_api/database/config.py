from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# 1. DB path setting
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "insider_threats.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# 2. Engine and Session setup
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 3. Tables Definition
class SystemLog(Base):
    __tablename__ = "system_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, index=True)
    ip_address = Column(String)
    action = Column(String)
    status = Column(String)
    is_threat = Column(Boolean, default=False)
    threat_type = Column(String, nullable=True)
    admin_feedback = Column(String, default="Pending")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) 

# 4. Create Tables
Base.metadata.create_all(bind=engine)
print("✅ Database configurations loaded and tables verified.")