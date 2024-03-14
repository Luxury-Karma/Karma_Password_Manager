import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt_file(password, filename, user_name):
    # Check if the salt file exists
    salt_file = f'salt_{user_name}.txt'
    if os.path.exists(salt_file):
        # If the salt file exists, read the salt
        with open(salt_file, 'rb') as f:
            salt = f.read()
    else:
        # If the salt file doesn't exist, generate a new salt and save it to a file
        salt = os.urandom(16)
        with open(salt_file, 'wb') as f:
            f.write(salt)

    # Derive a key from the password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    # Create a cipher object
    cipher_suite = Fernet(key)

    # Read the data from the file
    with open(filename, 'rb') as f:
        data = f.read()

    # Encrypt the data
    cipher_text = cipher_suite.encrypt(data)

    # Save the encrypted data to a file
    with open('encrypted_data.txt', 'wb') as f:
        f.write(cipher_text)



def decrypt_file(password, filename,user_name):
    # Read the salt from its file
    with open(f'salt_{user_name}.txt', 'rb') as f:
        salt = f.read()

    # Derive the key from the password and salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    # Create a cipher object
    cipher_suite = Fernet(key)

    # Read the encrypted data from its file
    with open(filename, 'rb') as f:
        cipher_text = f.read()

    # Decrypt the data
    plain_text = cipher_suite.decrypt(cipher_text)

    # Save the decrypted data to a file
    with open('decrypted_data.txt', 'wb') as f:
        f.write(plain_text)
