import json
import os

from server_modules import DB_Interactions


def main():
    DB_Interactions.__create_server_db(db_path='DB/server_user_db.db')


def is_free_username(testing_username:str)->bool:
    return DB_Interactions.user_verification(db_path='DB/server_user_db.db',user_to_verify=testing_username)


def create_user(user_name: str, salt, hash_verification)->bool:
    if not DB_Interactions.__create_new_server_user(db_path='DB/server_user_db.db', master_user_name=user_name, hash=hash_verification, salt=salt):
        print("Username already present in the database")
        return False

    DB_Interactions.create_user_db(db_path=f'user_data/{user_name}.db')
    return True


def add_new_password(user_name: str, website:str, password:str, website_user_name:str):
    DB_Interactions.add_password_to_db(db_path=f'user_data/{user_name}.db', password=password, website=website, creation_date='2024-09-28', website_user_name=website_user_name)

def get_password_for_website(user_name: str, website:str):
    return DB_Interactions.fetch_password_for_website(db_path=f'user_data/{user_name}.db', website='netflix')

def get_user_salt(user_name: str):
    salt_clean = DB_Interactions.get_user_salt(db_path='DB/server_user_db.db', master_user_name=user_name)
    salt_clean = salt_clean[0][0]
    return salt_clean


def get_user_hash(user_name: str):
    hash_clean = DB_Interactions.get_user_hash(db_path='DB/server_user_db.db', master_user_name=user_name)
    hash_clean = hash_clean[0][0]
    return hash_clean


def read_settings():
    with open('settings/server_setting.json', 'r') as f:
        return json.loads(f.read())


if __name__ == '__main__':
    main()
