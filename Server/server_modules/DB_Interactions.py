import os
import sqlite3


def __sql_workers(db_path: str):
    c = sqlite3.connect(db_path)
    return c, c.cursor()


def user_verification(db_path: str, user_to_verify: str) -> bool:
    connection, cursor = __sql_workers(db_path)
    cursor.execute("SELECT username FROM user_list")
    data = cursor.fetchall()
    connection.close()
    for e in data:
        if user_to_verify in e:
            print("user allready exist")
            return False
    return True


# Ensure the proper creation of the user table for its passwords
def create_user_db(db_path):
    connection, cursor = __sql_workers(db_path)
    try:
        sql_command = """CREATE TABLE user_password ( 
            website VARCHAR(30),
            username VARCHAR(30),
            password VARCHAR(20),   
            creation_date DATE);"""

        cursor.execute(sql_command)
    except:
        print("account already created")
    connection.close()


def __create_server_db(db_path: str):
    connection, cursor = __sql_workers(db_path)
    try:
        sql_command = """CREATE TABLE user_list (
        username VARCHAR(30),
        salt TINYBLOB,
        hash BLOB
        );
        """
        cursor.execute(sql_command)
        connection.commit()
        connection.close()
    except:
        print("db already existed")


def __create_new_server_user(db_path: str, master_user_name: str, hash, salt=os.urandom(32), ) -> bool:
    if not user_verification(db_path, master_user_name):
        return False
    connection, cursor = __sql_workers(db_path)
    cursor.execute('INSERT INTO user_list (username, salt, hash) VALUES (?, ?, ?);', (master_user_name, salt, hash))
    connection.commit()
    connection.close()
    return True


def get_user_salt(db_path: str, master_user_name: str):
    connection, cursor = __sql_workers(db_path)
    cursor.execute(f'SELECT salt FROM user_list WHERE username="{master_user_name}";')
    salt = cursor.fetchall()
    connection.close()
    return salt


def get_user_hash(db_path: str, master_user_name: str):
    connection, cursor = __sql_workers(db_path)
    cursor.execute(f'SELECT hash FROM user_list WHERE username="{master_user_name}";')
    hash = cursor.fetchall()
    connection.close()
    return hash


def add_password_to_db(db_path: str, website: str, website_user_name:str, password: str, creation_date: str):
    connection, cursor = __sql_workers(db_path)
    cursor.execute(f'INSERT INTO user_password VALUES ("{website}","{website_user_name}", "{password}", "{creation_date}")')
    connection.commit()
    connection.close()


def fetch_all_information(db_path: str):
    connection, cursor = __sql_workers(db_path)
    cursor.execute("SELECT * FROM user_password")
    data = cursor.fetchall()
    connection.close()
    return data


def fetch_all_website(db_path):
    connection, cursor = __sql_workers(db_path)
    cursor.execute("SELECT website FROM user_password")
    data = cursor.fetchall()
    connection.close()
    return data[0][0]

def fetch_password_for_website(db_path:str, website:str):
    connection, cursor = __sql_workers(db_path)
    cursor.execute('SELECT password FROM user_password')
    data = cursor.fetchall()
    connection.close()
    return data[0][0]


def update_password_for_specific_website(db_path: str, new_password: str, modification_date: str, website: str):
    connection, cursor = __sql_workers(db_path)
    cursor.execute(f'UPDATE user_password SET password = "{new_password}" WHERE website="{website}";')
    cursor.execute(f'UPDATE user_password SET creation_date = "{modification_date}" WHERE website="{website}";')
    connection.commit()
    connection.close()
