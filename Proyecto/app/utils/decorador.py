from cryptography.fernet import Fernet
from django.conf import settings
import base64

# Convertimos SECRET_KEY en una clave segura de 32 bytes
key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].encode())
fernet = Fernet(key)

def encrypt(value: str) -> str:

    return fernet.encrypt(str(value).encode()).decode()

def decrypt(token: str) -> str:

    return fernet.decrypt(token.encode()).decode()
