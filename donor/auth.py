import os
from donor.api_client import WemaAPI

TOKEN_FILE = os.path.expanduser("~/.wema_token")
BASE_URL = "http://localhost:5000"

def login(email, password):
    api = WemaAPI(BASE_URL)
    data = api.post("/api/admin/login", {
        "email": email,
        "password": password
    })

    token = data.get("token")
    if not token:
        raise Exception("Login failed")

    with open(TOKEN_FILE, "w") as f:
        f.write(token)

    print("✅ Logged in to Wema")

def load_token():
    if not os.path.exists(TOKEN_FILE):
        raise Exception("Please login first")
    with open(TOKEN_FILE) as f:
        return f.read().strip()
