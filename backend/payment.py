import requests
import os

def create_cashfree_session(email, phone):
    url = "https://sandbox.cashfree.com/pg/orders"
    headers = {
        "x-client-id": os.getenv("CASHFREE_ID"),
        "x-client-secret": os.getenv("CASHFREE_SECRET"),
        "Content-Type": "application/json"
    }
    payload = {
        "customer_details": {
            "customer_id": email,
            "customer_email": email,
            "customer_phone": phone
        },
        "order_amount": 999,
        "order_currency": "INR",
        "order_id": f"ORD_{email}",
        "order_note": "TallySmart Pro Plan"
    }
    r = requests.post(url, json=payload, headers=headers)
    return r.json()