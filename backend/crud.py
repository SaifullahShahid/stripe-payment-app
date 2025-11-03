from sqlalchemy.orm import Session
from . import models

def create_payment(db: Session, name: str, email: str, amount: int, currency: str):
    p = models.Payment(name=name, email=email, amount=amount, currency=currency, status="created")
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def update_payment_status(db: Session, stripe_pi_id: str, status: str):
    p = db.query(models.Payment).filter(models.Payment.stripe_pi_id == stripe_pi_id).first()
    if p:
        p.status = status
        db.add(p)
        db.commit()
        db.refresh(p)
    return p

def attach_stripe_id(db: Session, payment_id: int, stripe_pi_id: str):
    p = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if p:
        p.stripe_pi_id = stripe_pi_id
        db.add(p)
        db.commit()
        db.refresh(p)
    return p
