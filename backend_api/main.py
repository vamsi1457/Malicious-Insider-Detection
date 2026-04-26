from fastapi import FastAPI
import uvicorn
from api.routes import router

# API srustinchadam
app = FastAPI(title="Advanced Insider Threat API")

# Routes ni connect cheyadam
app.include_router(router)

# Basic health check (Browser lo check cheyadaniki)
@app.get("/")
def health_check():
    return {"status": "API is running securely. Ready to receive logs."}

if __name__ == "__main__":
    print("🚀 Starting Advanced API Server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)