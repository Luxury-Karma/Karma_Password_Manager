import os
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


from cryptography.fernet import InvalidToken


def encrypt_file(password, filename, user_name) -> bool:
    # Check if the salt file exists
    salt_file = f'salt_{user_name}.txt'
    if os.path.exists(salt_file):
        # If the salt file exists, read the salt
        try:
            with open(salt_file, 'rb') as f:
                salt = f.read()
        except IOError:
            print("Error reading salt file.")
            return False
    else:
        # If the salt file doesn't exist, generate a new salt and save it to a file
        salt = os.urandom(16)
        try:
            with open(salt_file, 'wb') as f:
                f.write(salt)
        except IOError:
            print("Error writing salt file.")
            return False

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
    try:
        with open(filename, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print("File to encrypt not found.")
        return False

    # Encrypt the data
    cipher_text = cipher_suite.encrypt(data)

    # Save the encrypted data to a file
    try:
        with open('encrypted_data.txt', 'wb') as f:
            f.write(cipher_text)
    except IOError:
        print("Error writing encrypted data to file.")
        return False

    print("File encrypted successfully.")
    return True


def decrypt_file(password, file_to_decrypt_path, user_name) -> bool:
    try:
        # Read the salt from its file
        with open(f'salt_{user_name}.txt', 'rb') as f:
            salt = f.read()
    except FileNotFoundError:
        print("Salt file not found.")
        return False

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

    try:
        # Read the encrypted data from its file
        with open(file_to_decrypt_path, 'rb') as f:
            cipher_text = f.read()
    except FileNotFoundError:
        print("File to decrypt not found.")
        return False

    try:
        # Decrypt the data
        plain_text = cipher_suite.decrypt(cipher_text)
    except InvalidToken:
        print("Invalid key or corrupted ciphertext.")
        return False

    try:
        # Save the decrypted data to a file
        with open(file_to_decrypt_path, 'wb') as f:
            f.write(plain_text)
    except IOError:
        print("Error writing to file.")
        return False

    print("File decrypted successfully.")
    return True

