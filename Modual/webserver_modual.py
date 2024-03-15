from flask import Flask, request, render_template
from Modual import Password_Management
app = Flask(__name__, template_folder='../HTML')


def get_website_options():
    # For demonstration purposes, I'm returning a static list here
    return ["Google", "Facebook", "Twitter", "Chat"]


@app.route('/')
def home():
    return render_template('home.html', name='Home Page', website_options=get_website_options())


def run_web_server():
    app.run()
