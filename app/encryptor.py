### encryptor.py (Handles encryption and decryption)
from cryptography.fernet import Fernet
import os
import json

KEY_FILE = "encryption.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

fernet = load_key()

def encrypt_data(data):
    return fernet.encrypt(json.dumps(data).encode()).decode()

def decrypt_data(encrypted_data):
    return json.loads(fernet.decrypt(encrypted_data.encode()).decode())