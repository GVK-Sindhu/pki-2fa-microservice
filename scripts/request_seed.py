import requests
import json

STUDENT_ID = "23A91A0595"

REPO_URL = "https://github.com/GVK-Sindhu/pki-2fa-microservice"

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

with open("student_public.pem", "r") as f:
    public_key = f.read()

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": REPO_URL,
    "public_key": public_key
}

print("Sending request to instructor API...")
response = requests.post(API_URL, json=payload, timeout=30)

print("\nStatus:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    data = response.json()
    encrypted_seed = data.get("encrypted_seed")
    if encrypted_seed:
        with open("encrypted_seed.txt", "w") as f:
            f.write(encrypted_seed)
        print("\nEncrypted seed saved to encrypted_seed.txt")
