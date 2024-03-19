import secrets

from Modual import Password_Management
import json
import requests
from oauthlib import oauth2
from flask import Flask, request, render_template, redirect, session, url_for

# region TEMPORARY USER KEEP
temp_user_password: str = 'test' #TODO: Not use test and use some unchangeable value of a google account to create a strong password (maybe?)
DB_FILE_PATH: str = './usr_data/' #TODO: Receive it as an argument
# endregion



read_client = Password_Management.open_json_file("D:\\projet\\api_files\\secret_token_webapp.json")
CLIENT_ID = read_client['installed']['client_id']   # IN ABSOLUTLY NO CASE PUT THE REAL ONE IN GIT
CLIENT_SECRET = read_client['installed']['client_secret']  # IN ABSOLUTLY NO CASE PUT THE REAL ONE IN GIT

DATA = {
    'response_type': "code",  # this tells the auth server that we are invoking authorization workflow
    'redirect_uri': "https://localhost:5000/home",
    # redirect URI https://console.developers.google.com/apis/credentials
    'scope': 'https://www.googleapis.com/auth/userinfo.email',  # resource we are trying to access through Google API
    'client_id': CLIENT_ID,  # client ID from https://console.developers.google.com/apis/credentials
    'prompt': 'consent'}  # adds a consent screen

URL_DICT = {
    'google_oauth': 'https://accounts.google.com/o/oauth2/v2/auth',  # Google OAuth URI
    'token_gen': 'https://oauth2.googleapis.com/token',  # URI to generate token to access Google API
    'get_user_info': 'https://www.googleapis.com/oauth2/v3/userinfo'  # URI to get the user info
}

# Create a Sign in URI
CLIENT = oauth2.WebApplicationClient(CLIENT_ID)
REQ_URI = CLIENT.prepare_request_uri(
    uri=URL_DICT['google_oauth'],
    redirect_uri=DATA['redirect_uri'],
    scope=DATA['scope'],
    prompt=DATA['prompt'])

app = Flask(__name__, template_folder='../HTML')


#region SCRIPT
def get_website_options(usr_name: str):
    Password_Management.look_user_files(usr_password=temp_user_password, usr_name=usr_name, db_file_path=DB_FILE_PATH)
    return Password_Management.get_all_website(usr_password=temp_user_password, usr_name=usr_name,
                                               db_path=f'{DB_FILE_PATH}/db_{usr_name}.json')


def add_new_website_action(email: str):
    """
    Get the name, password and note for a new website and add it to the DB of the user
    :return: None
    :rtype: None
    """
    new_website = request.form.get('new_website')
    new_password = request.form.get('new_password')
    random_password = True if request.form.get('randomize_password') == 'on' else False
    if random_password:
        new_password = Password_Management.generate_password()
    print(f'{random_password} IS THE PASSWORD RANDOMIZE')
    new_note = request.form.get('new_web_note')
    Password_Management.add_website(db_path=f'{DB_FILE_PATH}/db_{email}.json', usr_password=temp_user_password,
                                    usr_name=email, password=new_password, website_name=new_website,
                                    more_information=new_note)

    # VISUAL UPDATE (maybe do something else later
    # it is usefull that the user see its new shit
    password_dictionary = Password_Management.get_password_for_website(ask_website=[new_website],
                                                                       usr_password=temp_user_password,
                                                                       usr_name=email,
                                                                       db_path=f'{DB_FILE_PATH}db_{email}.json')
    return render_template('home.html', name='Home Page', website_options=get_website_options(usr_name=email),
                           website=new_website, password=password_dictionary[f"{new_website}"]["password"],
                           note=password_dictionary[f"{new_website}"]["note"], email=email)

def update_website_action(email: str):
    website = request.form.get('website')
    new_password = request.form.get('new_password')
    new_more_information = request.form.get('new_web_note')
    Password_Management.update_website(website_name=website, usr_password=temp_user_password, usr_name=email
                                       , db_path=f'{DB_FILE_PATH}/db_{email}.json', new_password=new_password,
                                       new_more_information=new_more_information)


def remove_website_action(email: str):
    website = request.form.get('website')
    Password_Management.remove_website(db_path=f'{DB_FILE_PATH}/db_{email}.json', website_name=website, usr_password=temp_user_password,
                                       usr_name=email)


#endregion


@app.route('/')
def login():
    "Home"
    # redirect to the newly created Sign-In URI
    return redirect(REQ_URI)


@app.route('/home')
def home():
    "Redirect after Google login & consent"

    # Get the code after authenticating from the URL
    code = request.args.get('code')

    # Generate URL to generate token
    token_url, headers, body = CLIENT.prepare_token_request(
        URL_DICT['token_gen'],
        authorisation_response=request.url,
        # request.base_url is same as DATA['redirect_uri']
        redirect_url=request.base_url,
        code=code)

    # Generate token to access Google API
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(CLIENT_ID, CLIENT_SECRET))

    # Parse the token response
    CLIENT.parse_request_body_response(json.dumps(token_response.json()))

    # Add token to the Google endpoint to get the user info
    # oauthlib uses the token parsed in the previous step
    uri, headers, body = CLIENT.add_token(URL_DICT['get_user_info'])

    # Get the user info
    response_user_info = requests.get(uri, headers=headers, data=body)
    info = response_user_info.json()

    # Store user's email in the session
    session['email'] = info['email']

    return redirect('/user/%s' % info['email'])


@app.route('/user/<email>')
def login_success(email):
    """Landing page after successful login"""

    # Check if the user is authenticated
    if 'email' not in session or session['email'] != email:
        # If not authenticated, redirect to the login page
        return redirect(url_for('login'))

    return render_template(template_name_or_list='home.html', name='Home Page',
                           website_options=get_website_options(email),email=email)


@app.route('/user/<email>/submit', methods=['POST'])
def submit(email):
    # Check if the user is authenticated
    if 'email' not in session or session['email'] != email:
        # If not authenticated, redirect to the login page
        print('WHO THE FUCK ARE YOU')
        return redirect(url_for('login'))
    action = request.form.get('action')
    if action == 'get_password':
        website = request.form.get('website')
        password_dictionary = Password_Management.get_password_for_website(ask_website=[website],
                                                                           usr_password=temp_user_password,
                                                                           usr_name=email,
                                                                           db_path=f'{DB_FILE_PATH}db_{email}.json')
        return render_template('home.html', name='Home Page', website_options=get_website_options(usr_name=email),
                               website=website, password=password_dictionary[f"{website}"]["password"],
                               note=password_dictionary[f"{website}"]["note"],email=email)
    elif action == 'submit':
        print('action chosen : submit')
        chosen_option = request.form.get('chosen_option')
        print(f'found chosen option = {chosen_option}')
        if chosen_option == 'new_web':
           return add_new_website_action(email)
        elif chosen_option == 'update_web':
            update_website_action(email)
            return redirect(f'/user/{email}')
        elif chosen_option == 'remove_web':
            remove_website_action(email)
            return redirect(f'/user/{email}')
    print('action is done')



#TODO: HANDLE NEW USER AND ADD THERE DATA BASE DURING RUNNING TIME TO THE CHECKUP



#region User Web Page

def run_web_server(port:int, debug:bool):
    # Set a secret key for the Flask application
    app.secret_key = secrets.token_hex(16)  # Generate a random 16-byte secret key
    app.run(debug=debug, host='0.0.0.0', port=port, ssl_context='adhoc')
#endregion


