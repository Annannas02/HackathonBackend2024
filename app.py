from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import webbrowser
import os

app = Flask(__name__, template_folder='templates')



CORS(app)


API_BASE = "https://92f1-77-89-208-34.ngrok-free.app/api/"

@app.route('/')
def home():
  return render_template('home.html')

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    api_url = "https://92f1-77-89-208-34.ngrok-free.app/api/authen/auth/register"
    response = requests.post(api_url, json={"username": username, "password": password})

    if response.ok:
        return jsonify({"message": "Registration successful"}), 200
    else:
        return jsonify({"error": "Registration failed", "details": response.json()}), response.status_code


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Step 1: Generate OTP
    otp_response = requests.post(
        "https://92f1-77-89-208-34.ngrok-free.app/api/authen/2fa/generateOtp",
        json={"username": username, "password": password},
    )
    if otp_response.status_code != 200:
        return jsonify({"error": "Failed to generate OTP", "details": otp_response.json()}), otp_response.status_code

    totp_code = otp_response.json().get("totp_code")

    # Step 2: Authenticate User
    auth_response = requests.post(
        "https://92f1-77-89-208-34.ngrok-free.app/api/authen/2fa/authenticate",
        json={"username": username, "totp_code": totp_code},
    )
    if auth_response.status_code == 200:
        tokens = auth_response.json()
        return jsonify({"message": "Login successful", "tokens": tokens}), 200
    else:
        return jsonify({"error": "Authentication failed", "details": auth_response.json()}), auth_response.status_code

@app.route('/book-reference')
def book():
    return render_template('book-reference.html')

@app.route('/email-assist')
def email():
    return render_template('email-assist.html')

@app.route('/recommendations')
def recommend():
    return render_template('recommend.html')



if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)

