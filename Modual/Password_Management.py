import os
from typing import List

from Modual import file_encryption_modual
from Modual import Password_creator_modual
import main
import json


def generate_password() -> str:
    return Password_creator_modual.generate_password(main.get_password_dictionary_path())


def get_usr_db_info(db_path: str, usr_password: str, usr_name: str ) -> dict:
    usr_db = file_encryption_modual.decrypt_information_from_file(file_to_decrypt_path=db_path, password=usr_password,
                                                                  user_name=usr_name)
    if usr_db == {"ERROR": True}:
        print("ERROR the file was not able to be decrypted")
        return {"ERROR": True}
    return usr_db


def encrypt_usr_db_info(usr_password: str, db_path: str, usr_name: str):
    if not file_encryption_modual.encrypt_file(password=usr_password, filename=db_path, user_name=usr_name):
        print("MAJOR ERROR WAS NOT ABLE TO ENCRYPT THE FILE")



def open_json_file(json_path: str) -> dict:
    json_information: dict = {}
    with open(json_path, 'r') as db:
        try:
            json_information = json.load(db)
        except json.JSONDecodeError as e:
            print(f"There is no Database loadable.\n ERROR :{e}")
        db.close()
    return json_information


def add_website(db_path: str, usr_name: str, usr_password: str, website_name: str, password: str,
                more_information: str):
    """
    Add a website with its password to the data base
    :param db_path: path to the user data base
    :param usr_name: name of the user
    :param usr_password: password of the user
    :param website_name: name of the new website
    :param password: password for the website
    :param more_information: any more information to let for the website
    :return: None
    :rtype: None
    """
    usr_db = get_usr_db_info(db_path=db_path, usr_password=usr_password, usr_name=usr_name)

    if usr_db == {"ERROR": True}:
        print("No data could be fetched")
        return

    Password_creator_modual.add_password_to_db(password=password, more_information=more_information,
                                               website=website_name,
                                               data_base_path=db_path)

    encrypt_usr_db_info(usr_password=usr_password, usr_name=usr_name, db_path=db_path)


def update_website(db_path: str, usr_name: str, usr_password: str, website_name: str, new_password: str,
                   new_more_information: str):
    """
    Change the information for the website given
    :param db_path: Path to the data base
    :param usr_name: name of the data base user
    :param usr_password: password of the data base user
    :param website_name: name of the website to update
    :param new_password: new password to the website
    :param new_more_information: new information to the website
    :return: None
    :rtype: None
    """
    usr_db = get_usr_db_info(db_path=db_path,usr_name=usr_name,usr_password=usr_password)

    website_information: dict = usr_db[website_name]

    if new_password == '' or new_password == None:
        new_password = website_information['password']
        print('No Need to change the password!')

    if new_more_information == '' or new_more_information == None:
        new_more_information = website_information['note']
        print('No need to change the more information!')

    website_information['note'] = new_more_information
    website_information['password'] = new_password
    usr_db[website_name] = website_information

    encrypt_usr_db_info(usr_password=usr_password,usr_name=usr_name,db_path=db_path)


def remove_website(db_path: str, usr_name: str, usr_password: str, website_name: str):
    usr_db = get_usr_db_info(db_path=db_path, usr_name=usr_name, usr_password=usr_password)
    usr_db.pop(website_name, None)
    encrypt_usr_db_info(usr_password=usr_password, usr_name=usr_name, db_path=db_path)


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
    if not file_encryption_modual.decrypt_file(file_to_decrypt_path=db_path, user_name=usr_name, password=usr_password):
        print("ERROR")
    db_info.update(open_json_file(db_path))
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
    print(f"DB PATH IS : {db_path}")
    password_asked: dict = {}
    usr_db = get_usr_db_info(usr_password=usr_password, usr_name=usr_name, db_path=db_path)

    for key, value in usr_db.items():
        if key not in ask_website:
            continue
        password_asked[key] = value

    return password_asked


def look_user_files(usr_name: str, usr_password: str, db_file_path: str):
    db_usr_path: str = f'{db_file_path}db_{usr_name}.json'
    db_usr_path_abs: str = os.path.abspath(db_usr_path)
    print(f"file location should be : {db_usr_path_abs}\n PATH RECEIVED: {db_usr_path}\nActive Directory {os.getcwd()}")
    if os.path.exists(db_usr_path_abs):
        print('User data exist ! yay')
        return
    random_dictionary = {'Whait this is empty!':{'password':'yes','note':'\'cause your dumb'}}
    with open(db_usr_path_abs, 'w') as db:
        json.dump(random_dictionary, db)
        db.close()
    file_encryption_modual.encrypt_file(password=usr_password, user_name=usr_name, filename=db_usr_path_abs)
    print(f'new database created for user {usr_name}')



