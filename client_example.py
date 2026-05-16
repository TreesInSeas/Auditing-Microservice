import requests
BASE_URL = "http://127.0.0.1:1234"

def add_to_audit_log(email, text):
    response = requests.post(
        f"{BASE_URL}/audit",
        json={"email": email, "text": text}
    )
    print("Status code:", response.status_code)
    print(response.json())
