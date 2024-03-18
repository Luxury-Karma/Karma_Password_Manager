from googleapiclient.discovery import build
from Modual import google_interaction
from Modual import webserver_modual


def main():
    calling_update()
    webserver_modual.run_web_server()


def calling_update():
    service = google_interaction.get_service()
    list_directory = google_interaction.get_files_and_id(service)
    google_interaction.update_backup(list_directory, service)
    google_interaction.print_all_files(service)
    google_interaction.download_file(file_id='11B4Qs7yJ2LNOx49TQ1rcdnsMSLDZdPKS', service=service, local_dest='D:\\projet\\does_it_work.txt')


def get_password_dictionary_path() -> list[str]:
    return ["D:\\projet\\apps\\test_comon_password.txt",
            "D:\\projet\\apps\\test_comon_password_three.txt",
            "D:\\projet\\apps\\test_comon_password_two.txt"]





def get_db_path() -> str:
    return '/db.json'


if __name__ == "__main__":
    main()
