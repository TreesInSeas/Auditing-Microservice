import requests
BASE_URL = "http://127.0.0.1:1234"

def add_to_audit_log(email, text):
    response = requests.post(
        f"{BASE_URL}/audit",
        json={"email": email, "text": text}
    )
    print("Status code:", response.status_code)
    print(response.json())
def get_audit_log(email=None):
    params = {}
    if email:
        params["email"] = email

    response = requests.get(f"{BASE_URL}/audit", params=params)
    print("Status code:", response.status_code)

    data = response.json()
    for log in data.get("logs", []):
        print(log["email"], "-", log["text"], "-", log["timestamp"])
