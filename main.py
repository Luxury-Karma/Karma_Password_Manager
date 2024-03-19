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
    backup_thread = threading.Thread(target=Backup, args=(args.time_to_backup,))
    backup_thread.start()
    webserver_modual.run_web_server(args.port, args.debug)


def Backup(time_in_minutes: int):
    server_backup = True
    #TODO:NEED TO ENSURE THE USERS FILES ARE ALL ENCRYPTED
    files_encrypted = True
    while server_backup:
        if files_encrypted:
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





def get_db_path() -> str:
    return '/db.json'


if __name__ == "__main__":
    main()
