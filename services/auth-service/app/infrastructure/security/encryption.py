from cryptography.fernet import Fernet
from app.config.settings import ENCRYPTION_KEY

cipher = Fernet(ENCRYPTION_KEY.encode())

def encrypt(value: str) -> str:
    return cipher.encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    return cipher.decrypt(value.encode()).decode()
