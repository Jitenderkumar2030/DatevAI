import requests

CASHFREE_CLIENT_ID = "YOUR_SANDBOX_CLIENT_ID"
CASHFREE_CLIENT_SECRET = "YOUR_SANDBOX_CLIENT_SECRET"
CASHFREE_PLAN_ID = "Plan_INR"
CASHFREE_AUTH_URL = "https://sandbox.cashfree.com/pg/auth/login"
CASHFREE_SUBSCRIPTION_URL = "https://sandbox.cashfree.com/pg/subscription/v1/create"

def create_subscription_session(email):
    try:
        # Auth Step
        auth_res = requests.post(
            CASHFREE_AUTH_URL,
            headers={"Content-Type": "application/json"},
            json={
                "client_id": CASHFREE_CLIENT_ID,
                "client_secret": CASHFREE_CLIENT_SECRET
            }
        )
        print("[DEBUG] Auth Response:", auth_res.status_code, auth_res.text)
        auth_data = auth_res.json()

        if "data" not in auth_data:
            print("[ERROR] Auth Failed:", auth_data)
            return None

        token = auth_data["data"]["token"]

        # Subscription Create Step
        session_res = requests.post(
            CASHFREE_SUBSCRIPTION_URL,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "x-api-version": "2022-09-01"
            },
            json={
                "customer_details": {
                    "customer_id": email,
                    "customer_email": email,
                    "customer_phone": "9999999999"
                },
                "subscription": {
                    "plan_id": CASHFREE_PLAN_ID,
                    "return_url": "http://localhost:8501?payment=success",
                    "subscription_note": "TallySmartAI Pro Access"
                }
            }
        )
        print("[DEBUG] Subscription Response:", session_res.status_code, session_res.text)

        session_data = session_res.json()
        return session_data["data"]["subscription_link"] if "data" in session_data else None

    except Exception as e:
        print("[EXCEPTION] Cashfree Error:", str(e))
        return None
