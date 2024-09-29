import hashlib
import os
import server_main
# --- Constants ---
SALT_LENGTH = 32  # 32 bytes for the salt
HASH_ITERATIONS = 100000  # Number of iterations for PBKDF2
HASH_LENGTH = 32  # Length of the derived hash (256 bits / 32 bytes)


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


# --- Simulating account creation and login ---
# Account creation
master_password = "my_secure_master_password"  # This would be entered by the user
master_username = "my_account"
account_data = create_account(master_username, master_password)

# Simulating login
entered_password = "my_secure_master_passwords"  # This would be entered by the user during login
is_authenticated = authenticate_user(username=master_username,entered_password=entered_password)
