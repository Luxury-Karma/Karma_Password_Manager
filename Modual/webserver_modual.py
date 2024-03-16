from flask import Flask, request, render_template, redirect
from Modual import Password_Management

app = Flask(__name__, template_folder='../HTML')

# region TEMPORARY USER KEEP
temp_user_name: str = 'test'
temp_user_password: str = 'test'
temp_db_path: str = 'db_test.json'


# endregion

def get_website_options():
    return Password_Management.get_all_website(usr_password=temp_user_password, usr_name=temp_user_name,
                                               db_path=temp_db_path)


@app.route('/')
def home():
    return render_template('home.html', name='Home Page', website_options=get_website_options())


def add_new_website_action():
    """
    Get the name, password and note for a new website and add it to the DB of the user
    :return: None
    :rtype: None
    """
    new_website = request.form.get('new_website')
    new_password = request.form.get('new_password')
    new_note = request.form.get('new_web_note')
    Password_Management.add_website(db_path=temp_db_path, usr_password=temp_user_password,
                                    usr_name=temp_user_name, password=new_password, website_name=new_website,
                                    more_information=new_note)


def update_website_action():
    website = request.form.get('website')
    new_password = request.form.get('new_password')
    new_more_information = request.form.get('new_web_note')
    Password_Management.update_website(website_name=website, usr_password=temp_user_password, usr_name=temp_user_name
                                       , db_path=temp_db_path, new_password=new_password,
                                       new_more_information=new_more_information)


def remove_website_action():
    website = request.form.get('website')
    Password_Management.remove_website(db_path=temp_db_path, website_name=website, usr_password=temp_user_password,
                                       usr_name=temp_user_name)


@app.route('/submit', methods=['POST'])
def submit():
    action = request.form.get('action')
    if action == 'get_password':
        if action == 'get_password':
            website = request.form.get('website')
            password_dictionary = Password_Management.get_password_for_website(ask_website=[website],
                                                                               usr_password=temp_user_password,
                                                                               usr_name=temp_user_name,
                                                                               db_path=temp_db_path)

            return render_template('home.html', name='Home Page', website_options=get_website_options(),
                                   website=website, password=password_dictionary[f"{website}"]["password"],
                                   note=password_dictionary[f"{website}"]["note"])
    elif action == 'submit':
        chosen_option = request.form.get('chosen_option')
        if chosen_option == 'new_web':
            add_new_website_action()

        elif chosen_option == 'update_web':
            update_website_action()

        elif chosen_option == 'remove_web':
            remove_website_action()
    return redirect('/')


def run_web_server():
    app.run()
