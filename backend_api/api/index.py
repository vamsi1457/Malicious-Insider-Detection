from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.operations import save_log_to_db
from ml_engine.inference import evaluate_log

router = APIRouter()

# Schema: Vache data format idi pakka undali, lekapothe API reject chesthundi
class LogEvent(BaseModel):
    timestamp: str
    user_id: str
    ip_address: str
    action: str
    status: str

@router.post("/api/v1/ingest_log")
def ingest_log(log: LogEvent):
    # 1. Pydantic nunchi normal dictionary ga marchadam
    log_dict = log.dict()
    
    # 2. ML Engine ki pampi, "Idi thappa? Oppa?" ani aduguthunnam
    is_threat, threat_type = evaluate_log(log_dict)
    
    # 3. Vachina result ni Database lo SAVE chesthunnam
    success = save_log_to_db(log_dict, is_threat, threat_type)
    
    if not success:
        raise HTTPException(status_code=500, detail="Database lo save avvaledu.")

    # 4. Terminal lo admin chudadaniki print chesthunnam
    if is_threat:
        print(f"🚨 [THREAT SAVED TO DB] User: {log.user_id} | Type: {threat_type}")
    else:
        print(f"✅ [NORMAL SAVED] User: {log.user_id}")

    return {"status": "success", "is_threat": is_threat}
