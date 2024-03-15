from Modual import file_encryption_modual
import json


def get_all_website(db_path: str, usr_name: str, usr_password: str) -> list[str]:
    """
    Go to see all the Website option from the DB
    :param db_path: Where is the DB
    :param usr_name: Witch User is Asking
    :param usr_password: What is the User Password to his DB
    :return: List of the website the user have
    :rtype: list[str]
    """
    all_website: list[str] = []
    db_info: dict = {}
    if not file_encryption_modual.decrypt_file(file_to_decrypt_path=db_path,user_name=usr_name,password=usr_password):
        print("ERROR")
    with open(db_path, 'r') as db:
        try:
            db_info = json.load(db)
        except json.JSONDecodeError as e:
            print(f"There is no Database loadable.\n ERROR :{e}")
        db.close()
    if not file_encryption_modual.encrypt_file(usr_password, db_path, usr_name):
        print("MAJOR ERROR NOT ABLE TO ENCRYPT THE FILE.")
    for key, value in db_info.items():
        all_website.append(key)
    return all_website


def get_password_for_website(db_path: str, usr_name: str, usr_password: str, ask_website: list[str]) -> dict:
    """
    Get password for website of a user
    :param db_path: path of his database
    :param usr_name: name of the user asking for his database
    :param usr_password: user password to access his database
    :param ask_website: list of the website we need the password
    :return: list of all the password asked
    :rtype: dict
    """
    password_asked: dict = {}
    db_information: dict = {}

    if not file_encryption_modual.decrypt_file(password=usr_password, user_name=usr_name, file_to_decrypt_path=db_path):
        print("ERROR NOT ABLE TO DECRYPT")
    with open(db_path, 'r') as db:
        try:
            db_information = json.load(db)
        except json.JSONDecodeError as e:
            print(f"There is no Database loadable.\n ERROR :{e}")
        db.close()
    if not file_encryption_modual.encrypt_file(usr_password, db_path, usr_name):
        print("MAJOR ERROR NOT ABLE TO ENCRYPT THE FILE.")

    for key, value in db_information.items():
        if key not in ask_website:
            continue
        password_asked[key] = value

    return password_asked
