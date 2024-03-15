import Password_creator_modual, file_encryption_modual
import json


def get_all_website(db_path: str, usr_name: str, usr_password: str) -> list[str]:
    all_website: list[str] = []
    db_info: dict = {}
    file_encryption_modual.decrypt_file(db_path, usr_name, usr_password)
    with open(db_path, 'r') as db:
        try:
            db_info = json.load(db)
        except json.JSONDecodeError as e:
            print(f"There is no Database loadable.\n ERROR :{e}")
            pass
    for key, value in db_info:
        all_website.append(key)
    return all_website
