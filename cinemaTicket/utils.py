import secrets


def generate_otp():
    return secrets.token_hex(3)
