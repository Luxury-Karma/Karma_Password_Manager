import json
import os
import time

from googleapiclient.discovery import build
from Modual import google_interaction
from Modual import webserver_modual
import argparse
import threading


def create_parser() -> argparse:
    my_parser = argparse.ArgumentParser(description='list of all the options of the application')
    my_parser.add_argument('-b', '--path_backup', type=str, required=True, help='The path to the backup directory')
    my_parser.add_argument('-a', '--admin_user', type=str, required=True, help='The JSON file for the Google Service Account')
    my_parser.add_argument('-w', '--web_token', type=str, required=True, help='Path to the secret token for the webapp API')
    my_parser.add_argument('-p', '--port', type=int, required=False, default=5000, help='Port you want the webserver running on. Base one on port 5000')
    my_parser.add_argument('-d', '--dictionary_path', type=str, required=False, help='The Directory where dictionary of comon password are kept')
    my_parser.add_argument('-t', '--time_to_backup', type=int, default=20, required=False, help='How often in minute do you want the server to backup its files. Base timer at 20 minutes')
    my_parser.add_argument('-db', '--debug', type=bool, default=False, required=False, help='If you want to activate flask DEBUG mode. Base option is False')
    my_parser.add_argument('-dl', '--download', type=bool, default=False, required=False, help='If you want to download the files from the backup')

    return my_parser.parse_args()


def main():

    args = create_parser()
    backup_thread = threading.Thread(target=backup, args=(args.time_to_backup, args.path_backup))
    backup_thread.start()
    webserver_modual.run_web_server(args.port, args.debug)

#TODO:CONTROL FILES WE SEND
def backup(time_in_minutes: int, backup_files_path: str):
    server_backup = True
    #TODO:NEED TO ENSURE THE USERS FILES ARE ALL ENCRYPTED
    files_encrypted = True
    while server_backup:
        list_none_backable_files = ensure_none_readable_json(backup_files_path)
        for e in [f for f in os.listdir(backup_files_path) if os.path.isfile(os.path.join(backup_files_path, f))]:
            service = google_interaction.get_service()
            list_directory = google_interaction.get_files_and_id(service)
            google_interaction.update_backup(list_directory, service)
            #google_interaction.print_all_files(service)
            #google_interaction.download_file(file_id='11B4Qs7yJ2LNOx49TQ1rcdnsMSLDZdPKS', service=service, local_dest='D:\\projet\\does_it_work.txt')
        time.sleep(60 * time_in_minutes)


def get_password_dictionary_path() -> list[str]:
    return ["D:\\projet\\apps\\test_comon_password.txt",
            "D:\\projet\\apps\\test_comon_password_three.txt",
            "D:\\projet\\apps\\test_comon_password_two.txt"]


def get_if_json_readable(file_path: str) -> bool:
    """
    This is use to look if we CAN open a file in a json format.
    Most use of this function is to see if we can freely get access to the json file.
    We will assume no one played with it for now. Because this would also say it is NOT readable even if a human COULD
    read it because the format is wrong
    """
    try:
        with open(file_path, 'r') as f:
            json.loads(f)
            return False
    except json.JSONDecodeError:
        return True


def ensure_none_readable_json(directory_path: str) -> list[str]:
    """
    This is a fall safe to ensure if someone manually decrypt a json and forgot the encrypt it we will not back it up.
    This should only affect the decrypted files. the other one should still be backed up
    """
    list_of_files = get_all_user_files(directory_path)
    list_of_readable_files = []
    for e in list_of_files:
        if not get_if_json_readable(e):
            continue
        list_of_readable_files.append(e)

    return list_of_readable_files


def get_all_user_files(usr_file_path: str) -> list[str]:
    """
        Look at the directory and get all the .json files
        :param usr_file_path: Where too look at
        :return: list of all the json in the directory
        :rtype: list[str]
    """
    return [f for f in os.listdir(usr_file_path) if os.path.isfile(f'{usr_file_path}\\{f}'
                                                              and os.path.splitext(f'{usr_file_path}\\{f}') == '.json')]  # look to all files that SHOULD be encrypted


if __name__ == "__main__":
    main()
