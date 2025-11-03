# FastAPI Backend - Stripe Payment App

---

## Description
- Create Stripe Payment Intents
- Handle Stripe Webhooks
- SQLite database with Alembic migrations
- Dockerized backend service
- Environment variables for Stripe keys and database URL

---

## Setup

1. Copy `.env.example` to `.env` and fill in your Stripe keys:

```
STRIPE_SECRET_KEY=<your_secret_key>
STRIPE_WEBHOOK_SECRET=<your_webhook_secret>
DATABASE_URL=sqlite:///./payments.db
```
Install dependencies (if running locally without Docker):

```
pip install -r requirements.txt
```
Apply database migrations:
```
alembic upgrade head
```
Run the backend locally:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

Docker
Build and run the backend service using Docker Compose:

```
docker-compose up --build backend
```

The backend API will be available at: http://localhost:8000
