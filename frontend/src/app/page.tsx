"use client";

import React, { useState } from "react";
import axios from "axios";
import { loadStripe } from "@stripe/stripe-js";
import {
  Elements,
  CardElement,
  useStripe,
  useElements,
} from "@stripe/react-stripe-js";

// Load Stripe with your publishable key
const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

// ----------------------
// Payment Form Component
// ----------------------
function CheckoutForm() {
  const stripe = useStripe();
  const elements = useElements();

  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    amount: "",
  });

  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/create-payment`,
        formData
      );

      const clientSecret = res.data.clientSecret;

      if (!stripe || !elements) return;

     
      const result = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: elements.getElement(CardElement)!,
          billing_details: {
            name: formData.fullName,
            email: formData.email,
          },
        },
      });

      if (result.error) {
        setMessage(`❌ Payment failed: ${result.error.message}`);
      } else if (result.paymentIntent?.status === "succeeded") {
        setMessage("✅ Payment successful! Thank you.");
      }
    } catch (error: any) {
      console.error(error);
      setMessage("❌ Something went wrong while processing payment.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-10 p-6 shadow-lg rounded-xl bg-white text-black">
      <h2 className="text-2xl font-semibold mb-4 text-center">Stripe Payment</h2>

      <input
        type="text"
        name="fullName"
        placeholder="Full Name"
        required
        value={formData.fullName}
        onChange={handleChange}
        className="w-full p-2 mb-3 border rounded"
      />

      <input
        type="email"
        name="email"
        placeholder="Email"
        required
        value={formData.email}
        onChange={handleChange}
        className="w-full p-2 mb-3 border rounded"
      />

      <input
        type="number"
        name="amount"
        placeholder="Amount (in USD)"
        required
        value={formData.amount}
        onChange={handleChange}
        className="w-full p-2 mb-4 border rounded"
      />

      <CardElement className="p-3 border rounded mb-4" />

      <button
        type="submit"
        disabled={!stripe || loading}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded"
      >
        {loading ? "Processing..." : "Pay Now"}
      </button>

      {message && (
        <p
          className={`mt-4 text-center ${
            message.startsWith("✅") ? "text-green-600" : "text-red-600"
          }`}
        >
          {message}
        </p>
      )}
    </form>
  );
}

export default function Page() {
  return (
    <Elements stripe={stripePromise}>
      <CheckoutForm />
    </Elements>
  );
}
