from googleapiclient.discovery import build
from Modual import goolge_interaction
from Modual import Password_creator_modual
from Modual import webserver_modual
from Modual import Password_Management
from Modual import file_encryption_modual

def main():
    # calling_update()
    generate_password()
    file_path_temp = "db_test.json"

    print(f"DEBUG WEBSITE LIST:"
          f"\n{Password_Management.get_all_website(usr_password='test',usr_name='test',db_path=file_path_temp)}\n")
    print(f"DEBUG PASSWORD LIST:"
          f"\n{Password_Management.get_password_for_website(usr_password='test',usr_name='test',db_path=file_path_temp,ask_website=['google.com','Facebook.com','Pornhub.com'])}\n")

    webserver_modual.run_web_server()


def calling_update():
    goolge_interaction.google_token_start()
    service: build = goolge_interaction.get_service()
    all_files: dict = goolge_interaction.get_files_and_id(service)
    goolge_interaction.update_backup(all_files, service)


def generate_password() -> str:
    return Password_creator_modual.generate_password(["D:\\projet\\apps\\test_comon_password.txt",
                                                      "D:\\projet\\apps\\test_comon_password_three.txt",
                                                      "D:\\projet\\apps\\test_comon_password_two.txt"])


def get_db_path() -> str:
    return '/db.json'


if __name__ == "__main__":
    main()
