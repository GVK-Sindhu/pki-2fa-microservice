from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import time

from app.crypto_utils import load_private_key, decrypt_seed
from app.totp_utils import generate_totp_code, verify_totp_code

DATA_DIR = "/data"
SEED_FILE = f"{DATA_DIR}/seed.txt"

app = FastAPI()


class DecryptRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


@app.post("/decrypt-seed")
def decrypt_seed_endpoint(req: DecryptRequest):
    try:
        private_key = load_private_key("student_private.pem")
        seed = decrypt_seed(req.encrypted_seed, private_key)

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(seed)

        return {"status": "ok"}

    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")


@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE, "r") as f:
        seed = f.read().strip()

    code = generate_totp_code(seed)

    valid_for = 30 - (int(time.time()) % 30)

    return {
        "code": code,
        "valid_for": valid_for
    }


@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE, "r") as f:
        seed = f.read().strip()

    valid = verify_totp_code(seed, req.code)

    return {"valid": valid}
