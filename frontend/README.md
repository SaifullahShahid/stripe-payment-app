# Next.js Frontend - Stripe Payment App

---

## Description
- User details form
- Stripe Elements integration for secure payments
- Calls backend API to create payment intents
- Displays payment success confirmation
- Dockerized frontend service

---

## Setup

1. Copy `.env.local.example` to `.env.local` and fill in your backend URL and Stripe public key:

```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=<your_stripe_public_key>
```

Install dependencies:
```
npm install
```

Run the frontend locally:
```
npm run dev
```

The frontend will be available at: http://localhost:3000

---

### Docker
Build and run the frontend service using Docker Compose:

```
docker-compose up --build frontend
```