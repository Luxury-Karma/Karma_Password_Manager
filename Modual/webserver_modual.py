from flask import Flask, request, render_template, redirect
from Modual import Password_Management
app = Flask(__name__, template_folder='../HTML')


def get_website_options():
    return Password_Management.get_all_website(usr_password='test',usr_name='test', db_path="db_test.json")


@app.route('/')
def home():
    return render_template('home.html', name='Home Page', website_options=get_website_options())


@app.route('/submit', methods=['POST'])
def submit():

    action = request.form.get('action')
    if action == 'get_password':
        if action == 'get_password':
            website = request.form.get('website')
            password_dictionary = Password_Management.get_password_for_website(ask_website=[website], usr_password='test',
                                                                    usr_name='test',
                                                                    db_path='db_test.json')
            print(f'Website : {website} \npassword is : {password_dictionary[f"{website}"]["password"]}\nNote is: {password_dictionary[f"{website}"]["note"]}')

            return render_template('home.html',name='Home Page',website_options=get_website_options(), website=website, password=password_dictionary[f"{website}"]["password"], note=password_dictionary[f"{website}"]["note"])
    elif action == 'submit':
        chosen_option = request.form.get('chosen_option')
        if chosen_option == 'new_web':
            new_website = request.form.get('new_website')
            new_password = request.form.get('new_password')
            print(f'adding website {new_website} with the password {new_password}')

        elif chosen_option == 'update_web':
            website = request.form.get('website')
            new_password = request.form.get('new_password')
            print(f'updating website {website} password to {new_password}')

        elif chosen_option =='remove_web':
            website = request.form.get('website')
            print(f"removing website :{website}")
    return redirect('/')


def run_web_server():
    app.run()
