import os.path
import random
import string
import re
import json



def generate_password(dictionary_path: list[str]) -> str:
    """
    Generate a secure password with alphanumeric character and special character.
    :param dictionary_path: Path of comon use password
    :return: a safe password
    :rtype: str
    """
    password = "".join(
        random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(random.randint(10, 20)))
    common_password = load_password_dictionaries(dictionary_path)
    while not check_password_strength(password, common_password):
        password = "".join(
            random.choice(string.ascii_letters + string.digits + string.punctuation) for i in
            range(random.randint(10, 20)))

    return password


def load_password_dictionaries(files: list[str]) -> set[str]:
    """
    Open multiple text files and split them in a list of individual word at every \n
    :param files: list of the path of the password dictionaries
    :return: a list of all the words inside the files
    :rtype: set[str]
    """
    common_passwords = set()
    for file in files:
        with open(file, 'r') as f:
            common_passwords.update(f.read().splitlines())
    return common_passwords


def check_password_strength(password: str, common_passwords: set[str]) -> bool:
    """
    Verify that the password is up to standard
    :param common_passwords: list of all the common used password the server have access to
    :param password: string to ensure is secure
    :return: true : password safe | false : password unsafe
    :rtype: bool
    """
    if password in common_passwords:
        return False
    pattern = (
        r'^(?=.*[0-9])'  # At least one digit
        r'(?=.*[a-z])'  # At least one lowercase letter
        r'(?=.*[A-Z])'  # At least one uppercase letter
        r'(?=.*[!@#$%^&*(),.?":{}|<>])'  # At least one special character
        r'(?!.*(.)\1\1)'  # No three consecutive identical characters
        r'.{8,}$'  # At least 8 characters long
    )  # Ensure basic password security
    return bool(re.match(pattern, password))  # Verify and return the strength of the password


def make_password_format(website: str, more_information: str, password: str) -> dict:
    """
    Make the format to conserve the password in the bank
    :param website: for witch website is this password
    :param more_information: Any information we would like to keep for this website
    :param password: the password for the website
    :return: the formatted password to conserve
    :rtype: dict
    """
    return {
        f"{website}": {
            "note": more_information,
            "password": password
        }
    }


def add_password_to_db(password: str, more_information: str, website: str, data_base_path: str) -> bool:
    """
    Correctly format and place the password inside the db
    :param password: password for the website
    :param more_information: any good information to have about the website
    :param website: where will this password be use
    :param data_base_path: where is the db file
    :return: If we could update it or not
    :rtype: bool
    """
    new_password = make_password_format(website, more_information, password)
    if not os.path.exists(data_base_path):
        open(data_base_path, 'x').close()

    db_info: dict = {}
    with open(data_base_path, 'r') as db:
        try:
            db_info = json.load(db)
        except json.JSONDecodeError:
            pass

    db_info.update(new_password)

    with open(data_base_path, 'w') as db:
        try:
            json.dump(db_info, db)
        except (TypeError, OSError) as e:
            print(f"Could not save the password due to error: {e}")
            return False

    return True