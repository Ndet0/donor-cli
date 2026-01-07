from donor.api_client import WemaAPI
from donor.auth import load_token

BASE_URL = "http://localhost:5000"

class DonorManager:
    def __init__(self):
        token = load_token()
        self.api = WemaAPI(BASE_URL, token)

    def list_donations(self):
        donations = self.api.get("/api/donations")
        for d in donations:
            print(f"{d['name']} | {d['amount']} | {d['createdAt']}")

    def add_donation(self, name, amount):
        self.api.post("/api/donations", {
            "name": name,
            "amount": amount
        })
        print("✅ Donation recorded")
