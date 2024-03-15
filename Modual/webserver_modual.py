from flask import Flask, request, render_template
from Modual import Password_Management
app = Flask(__name__, template_folder='../HTML')


def get_website_options():
    return Password_Management.get_all_website(usr_password='test',usr_name='test', db_path="db_test.json")


@app.route('/')
def home():
    return render_template('home.html', name='Home Page', website_options=get_website_options())


def run_web_server():
    app.run()
