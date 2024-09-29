import server_main
import os
import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode
import string
import random

# --- Constants ---
SALT_LENGTH = 32  # 32 bytes for the salt
HASH_ITERATIONS = 100000  # Number of iterations for PBKDF2
HASH_LENGTH = 32  # Length of the derived hash (256 bits / 32 bytes)
AES_KEY_LENGTH = 32  # AES-256 key length (32 bytes)


# TODO: THIS IS TEMPORARY JUST TO DEMO HOW THE COMMUNICATION WILL GO WITHOUT NETWORKING AND NOT IN THE PROPER LANGUAGE

# Function to generate a random salt
def generate_salt():
    return os.urandom(SALT_LENGTH)


# Function to hash the password with a salt using PBKDF2
def hash_password(master_password: str, salt: bytes):
    # PBKDF2_HMAC with SHA-256
    return hashlib.pbkdf2_hmac(
        'sha256',  # Hashing algorithm
        master_password.encode('utf-8'),  # Convert password to bytes
        salt,  # Salt (unique for each user)
        HASH_ITERATIONS,  # Number of iterations (higher is better for security)
        dklen=HASH_LENGTH  # Derived key length
    )


# Function to derive an AES encryption key from the master password
def derive_key(master_password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=AES_KEY_LENGTH,
        salt=salt,
        iterations=HASH_ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(master_password.encode('utf-8'))


# Function to encrypt a password using AES
def encrypt_password(master_password: str, password: str):
    salt = generate_salt()  # Generate a unique salt for the AES key
    key = derive_key(master_password, salt)  # Derive the AES key from the master password
    iv = os.urandom(16)  # Generate a random initialization vector

    # Encrypt the password
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the password to be a multiple of the block size (16 bytes for AES)
    padded_password = password.encode('utf-8') + b'\0' * (16 - len(password) % 16)
    encrypted_password = encryptor.update(padded_password) + encryptor.finalize()

    # Store the encrypted password along with the salt and IV (for decryption later)
    return urlsafe_b64encode(salt + iv + encrypted_password).decode('utf-8')


# Function to decrypt a password using AES
def decrypt_password(master_password: str, encrypted_data: str):
    data = urlsafe_b64decode(encrypted_data.encode('utf-8'))

    # Extract salt, IV, and encrypted password from the stored data
    salt = data[:SALT_LENGTH]
    iv = data[SALT_LENGTH:SALT_LENGTH + 16]  # IV is 16 bytes
    encrypted_password = data[SALT_LENGTH + 16:]

    key = derive_key(master_password, salt)  # Derive the AES key from the master password

    # Decrypt the password
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_password = decryptor.update(encrypted_password) + decryptor.finalize()

    # Remove padding (null bytes)
    return padded_password.rstrip(b'\0').decode('utf-8')


# Example: Creating an account (account registration)
def create_account(username, master_password: str):
    if not server_main.is_free_username(username):
        print('username already in use please select a new one')
        return

    salt = generate_salt()  # Generate a unique salt for the user
    password_hash = hash_password(master_password, salt)  # Hash the master password with the salt

    # Store the salt and password hash (these would be saved to the database in a real scenario)
    server_main.create_user(salt=salt, user_name=username, hash_verification=password_hash)
    print("Account created!")


# Example: Authenticating a user during login
def authenticate_user(username: str, entered_password: str):
    # Hash the entered password using the stored salt
    salt = server_main.get_user_salt(username)
    hash = server_main.get_user_hash(username)
    entered_hash = hash_password(entered_password, salt)

    # Compare the hash from the entered password with the stored hash
    if entered_hash == hash:
        print("Authentication successful!")
        return True

    print("Authentication failed. Invalid password.")
    return False


def generate_random_password(password_length: int = 50):
    letters = string.printable
    return ''.join(random.choice(letters) for i in range(password_length))


# --- Simulating account creation and login ---
# Account creation
master_password = "my_secure_master_password"  # This would be entered by the user
master_username = "my_account"
account_data = create_account(master_username, master_password)

# Simulating login
entered_password = "my_secure_master_passwords"  # This would be entered by the user during login
is_authenticated = authenticate_user(username=master_username,entered_password=entered_password)

encrypted_password = encrypt_password(password='password', master_password=master_password)

print(f'encrypted password = {encrypted_password}')

server_main.add_new_password(website='netflix', password=encrypted_password,user_name=master_username,website_user_name='i am a user')

print(f'original password : {decrypt_password(master_password=master_password, encrypted_data=server_main.get_password_for_website(master_username, "netflix"))}')


