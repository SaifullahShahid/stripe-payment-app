import os
import stripe
import schemas
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        name=user.name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


stripe.api_key = os.getenv("STRIPE_SECRET_KEY")



class PaymentRequest(BaseModel):
    fullName: str
    email: str
    amount: float


@app.post("/create-payment")
async def create_payment(request: PaymentRequest):
    try:
        
        amount_cents = int(request.amount * 100)

        
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="usd",
            receipt_email=request.email,
            metadata={"customer_name": request.fullName},
        )

        return {"clientSecret": intent.client_secret}

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/webhook")
async def webhook_received(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    
    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        print(f"✅ Payment succeeded for {intent['id']}")
    elif event["type"] == "payment_intent.payment_failed":
        print(f"❌ Payment failed")

    return {"status": "success"}
