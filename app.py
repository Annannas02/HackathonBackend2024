from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import webbrowser
import os

app = Flask(__name__, template_folder='templates')



CORS(app)
@app.route('/')
def home():
  return render_template('home.html')

@app.route('/book-reference')
def book():
    return render_template('book-reference.html')

@app.route('/email-assist')
def email():
    return render_template('email-assist.html')

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
