from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    with open("secret.key", "rb") as key_file:
        return Fernet(key_file.read())

def encrypt_data(data, fernet):
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data, fernet):
    return fernet.decrypt(data.encode()).decode()
