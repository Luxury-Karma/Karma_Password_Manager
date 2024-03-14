from flask import Flask, request
app = Flask(__name__)

@app.route('/update_password', methods=['POST'])
def update_password():
    username = request.form.get('username')
    password = request.form.get('password')
    website = request.form.get('website')
    # Call your Python script here, or move its functionality into this script
    return "Password updated successfully"


def run_web_server():
    app.run()
