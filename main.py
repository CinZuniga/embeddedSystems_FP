# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def greet():
    return "Hello, World!"

@app.route("/health")
def health():
    x = 1+1  # This line is intentionally left incomplete to simulate an error
    return "<p>Server is up and running.<p>"