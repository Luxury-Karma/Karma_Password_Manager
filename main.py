from googleapiclient.discovery import build
from Modual import goolge_interaction
from Modual import Password_creator_modual
from Modual import webserver_modual


def main():
    # calling_update()
    generate_password()
    webserver_modual.run_web_server()


def calling_update():
    goolge_interaction.google_token_start()
    service: build = goolge_interaction.get_service()
    all_files: dict = goolge_interaction.get_files_and_id(service)
    goolge_interaction.update_backup(all_files, service)


def generate_password():
    print(Password_creator_modual.generate_password(["D:\\projet\\apps\\test_comon_password.txt",
                                                     "D:\\projet\\apps\\test_comon_password_three.txt",
                                                     "D:\\projet\\apps\\test_comon_password_two.txt"]))


def get_db_path() -> str:
    return '/db.json'


if __name__ == "__main__":
    main()
