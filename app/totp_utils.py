import base64
import pyotp


def _hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode("utf-8")


def generate_totp_code(hex_seed: str) -> str:
    base32_seed = _hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    base32_seed = _hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=valid_window)
