from flask import Flask, request, render_template
app = Flask(__name__, template_folder='../HTML')


@app.route('/update_password', methods=['POST'])
def update_password():
    username = request.form.get('username')
    password = request.form.get('password')
    website = request.form.get('website')
    # Call your Python script here, or move its functionality into this script
    return "Password updated successfully"


@app.route('/')
def home():
    return render_template('home.html', name='Home Page')


def run_web_server():
    app.run()
