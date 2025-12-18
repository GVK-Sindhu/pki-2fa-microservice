#!/usr/bin/env python3
import sys
sys.path.append("/app")

import os
from datetime import datetime, timezone
from app.totp_utils import generate_totp_code

SEED_FILE = "/data/seed.txt"
LOG_FILE = "/cron/last_code.txt"

def main():
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists(SEED_FILE):
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} - Seed not available yet\n")
        return

    try:
        with open(SEED_FILE, "r") as f:
            hex_seed = f.read().strip()

        code = generate_totp_code(hex_seed)

        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} - 2FA Code: {code}\n")

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} - Error: {e}\n")

if __name__ == "__main__":
    main()

