import json
import os
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


from cryptography.fernet import InvalidToken


DB_FILE_PATH = './usr_data/'


def open_salt(usr_name: str) -> bytes:

    salt_file = os.path.abspath(f'{DB_FILE_PATH}salt_{usr_name}.txt')
    salt: bytes = b''
    if not os.path.exists(salt_file):
        # If the salt file doesn't exist, generate a new salt and save it to a file
        salt = os.urandom(16)
        try:
            with open(salt_file, 'wb') as f:
                f.write(salt)
                f.close()
        except IOError:
            print("Error writing salt file.")
            return salt

    # If the salt file exists, read the salt
    try:
        with open(salt_file, 'rb') as f:
            salt = f.read()
            f.close()
    except IOError:
        print(f"Salt file not found. for user : {usr_name}")
        return salt

    return salt

def derive_salt(salt):
    return PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )


def encrypt_file(password, filename, user_name) -> bool:
    # Check if the salt file exists

    salt = open_salt(usr_name=user_name)
    if salt == b'':
        print('Error no salt loaded')
        return False

    # Derive a key from the password
    key = base64.urlsafe_b64encode(derive_salt(salt).derive(password.encode()))

    # Create a cipher object
    cipher_suite = Fernet(key)

    # Read the data from the file
    file_abs_path = os.path.abspath(filename)
    try:
        with open(file_abs_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print("File to encrypt not found.")
        return False

    # Encrypt the data
    cipher_text = cipher_suite.encrypt(data)

    # Save the encrypted data to a file
    try:
        with open(file_abs_path, 'wb') as f:
            f.write(cipher_text)
    except IOError:
        print("Error writing encrypted data to file.")
        return False

    print("File encrypted successfully.")
    return True


def decrypt_file(password, file_to_decrypt_path, user_name) -> bool:
    """
    Make the file fully human readable. This should not be use for the interaction with the user. This function should be
    use if the server die and you need to switch the server informations or what ever other reason you want it readable.
    """
    salt = open_salt(usr_name=user_name)
    if salt == b'':
        print('Error no salt loaded')
        return False

    # Derive the key from the password and salt
    key = base64.urlsafe_b64encode(derive_salt(salt).derive(password.encode()))

    # Create a cipher object
    cipher_suite = Fernet(key)

    try:
        file_to_decrypt_path_abs = os.path.abspath(file_to_decrypt_path)
        # Read the encrypted data from its file
        with open(file_to_decrypt_path_abs, 'rb') as f:
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
        with open(file_to_decrypt_path_abs, 'wb') as f:
            f.write(plain_text)
    except IOError:
        print("Error writing to file.")
        return False

    print("File decrypted successfully.")
    return True


def decrypt_information_from_file(password, file_to_decrypt_path, user_name) -> dict:
    """
    This load one of the encrypted json file and decrypt it for user usages. This is only reading the file and returning the json
    """
    salt = open_salt(usr_name=user_name)
    if salt == b'':
        print('Error no salt loaded')
        return {}

    # Derive the key from the password and salt
    key = base64.urlsafe_b64encode(derive_salt(salt).derive(password.encode()))

    # Create a cipher object
    cipher_suite = Fernet(key)

    try:
        file_to_decrypt_path_abs = os.path.abspath(file_to_decrypt_path)
        # Read the encrypted data from its file
        with open(file_to_decrypt_path_abs, 'rb') as f:
            cipher_text = f.read()
    except FileNotFoundError:
        print("File to decrypt not found.")
        return {}

    try:
        # Decrypt the data
        plain_text = cipher_suite.decrypt(cipher_text)
    except InvalidToken:
        print("Invalid key or corrupted ciphertext.")
        return {}

    return json.loads(plain_text)


def encrypt_information_to_file(usr_password, data_to_encrypt, file_to_save, usr_name) -> bool:
    """
    This function encrypts a dictionary and saves it to a file. The file is never saved in its decrypted version.
    """
    salt = open_salt(usr_name=usr_name)
    if salt == b'':
        print('Error no salt loaded')
        return False

    # Derive the key from the password and salt
    key = base64.urlsafe_b64encode(derive_salt(salt).derive(usr_password.encode()))

    # Create a cipher object
    cipher_suite = Fernet(key)

    # Convert the dictionary into a JSON string
    data_str = json.dumps(data_to_encrypt)

    try:
        # Encrypt the data
        cipher_text = cipher_suite.encrypt(data_str.encode('utf-8'))
    except InvalidToken:
        print("Invalid key or corrupted plaintext.")
        return False

    try:
        file_to_save_path_abs = os.path.abspath(file_to_save)
        # Write the encrypted data to its file
        with open(file_to_save_path_abs, 'wb') as f:
            f.write(cipher_text)
    except FileNotFoundError:
        print("File to save not found.")
        return False

    return True
