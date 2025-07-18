from fastapi import FastAPI, File, UploadFile, Header, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import jwt
from utils import preprocess, predict_sales
from auth import verify_token
from models import SessionLocal, User  # ✅ Make sure you have this

SECRET = "testsecret"  # 🔒 Same as used in auth.py

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# 🔐 Verify token endpoint
@app.post("/verify")
def verify(data: dict):
    try:
        payload = jwt.decode(data["token"], SECRET, algorithms=["HS256"])
        return payload
    except:
        return {"error": "unauthorized"}


# 📊 Forecast prediction endpoint (Pro/Admin only)
@app.post("/predict")
def predict(file: UploadFile = File(...), authorization: str = Header(None)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return {"error": "unauthorized"}

    if payload["role"] not in ["pro", "admin"]:
        return {"error": "Upgrade to Pro to access forecasting."}

    df = pd.read_csv(file.file)
    df = preprocess(df)
    forecast = predict_sales(df)
    return forecast.tail(5).to_dict(orient="records")


# 💳 Webhook from Cashfree to auto-upgrade user
@app.post("/cashfree-webhook")
async def cashfree_webhook(request: Request):
    body = await request.body()
    try:
        data = json.loads(body)
        print("✅ Cashfree Webhook Payload:", data)
    except:
        return {"error": "Invalid JSON"}

    if data.get("event") == "SUBSCRIPTION_ACTIVATED":
        email = data["data"]["customer_details"]["customer_email"]
        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.role = "pro"
            db.commit()
        db.close()

    return {"status": "ok"}
