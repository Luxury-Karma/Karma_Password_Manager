from flask import Flask, redirect, url_for, request, render_template, jsonify, make_response
import hashlib
import os
import server_main
import uuid

app = Flask(__name__)

active_sessions = {}

def get_user_information(username: str):
    return {
        'salt': server_main.get_user_salt(user_name=username),
        'hash': server_main.get_user_hash(user_name=username)
    }


# Example of how you might create a hash when creating a user
def hash_password(master_password: str, salt: bytes):
    return hashlib.pbkdf2_hmac('sha256', master_password.encode('utf-8'), salt, 100000)


@app.route('/')
def loggin():
    return redirect('/login')


#TODO : WE NEED TO CLEAN WHAT THE USER SEND US ! we need to protect against sql injection
@app.route('/create', methods=['POST', 'GET'])
def create_account():
    if request.method == 'POST':
        # Receive and process the incoming JSON data
        data = request.get_json()

        if data:
            username = data.get('username')
            hashed_password = data.get('hashedPassword')
            salt = data.get('salt')

            if not server_main.is_free_username(username):
               return jsonify({'error': 'user already exist'}), 400

            server_main.create_user(user_name=username, hash_verification=hashed_password, salt=salt)

            return jsonify({'message': 'Account created successfully!'}), 201
        else:
            return jsonify({'error': 'Invalid data received!'}), 400

    return render_template('create_account.html')


@app.route('/salt_request', methods=['POST'])
def get_user_salts():
    if not request.method == 'POST':
        print("this is not a post request! ")
        return jsonify({'Error': 'Wrong Request'}), 404
    username = request.get_json()['username']
    user_salt = server_main.get_user_salt(username)
    if user_salt == None:
        return jsonify({'Error': 'User does not exist'}), 400
    print(f'user salt {user_salt}')
    return jsonify({'salt': user_salt}), 200


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.get_json()['username']
        hash = request.get_json()['hash']

        if not server_main.verify_user_hash(username, hash):
            return jsonify({'Error': 'Wrong password'}), 400

        # Once connected, generate the session id and send the cookie
        session_id = str(uuid.uuid4())
        active_sessions[session_id] = username

        # Create the cookie
        response = make_response(jsonify({'message': 'Login successful', 'redirect': f'/home/{username}'}))
        response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=900, samesite='None')

        return response
    return render_template('login.html')


@app.route('/verify', methods=['POST'])
def verify():
    username = request.json.get('un')
    client_hash = bytes.fromhex(request.json.get('hash'))

    user_info = get_user_information(username)

    if user_info:
        salt = user_info['salt']
        stored_hash = user_info['hash']  # Get the hash from your DB

        # Recreate the hash on the server
        hash_to_verify = hash_password(client_hash.decode(), salt)

        if hash_to_verify == stored_hash:
            print("user was able to connect")
            return jsonify({'message': 'Verification successful!'}), 200
        else:
            return jsonify({'message': 'Verification failed!'}), 401

    return jsonify({'message': 'User not found'}), 404


# Dynamic route for serving user-specific home page
@app.route('/home/<username>', methods=['GET'])
def user_home(username):
    print("hello personal home page")

    session_id = request.cookies.get('session_id')

    # Ensure the session is valid
    if session_id not in active_sessions or active_sessions[session_id] != username:
        return redirect('/login')

    # Render the user's specific home page (or JSON data for AJAX calls)
    return render_template('user_home.html')


# Example route for logging out (removes the session)
@app.route('/logout', methods=['POST'])
def logout():
    session_id = request.cookies.get('session_id')
    if session_id in active_sessions:
        del active_sessions[session_id]

    response = make_response(redirect('/login'))
    response.delete_cookie('session_id')
    return response

if __name__ == '__main__':
    app.run()
