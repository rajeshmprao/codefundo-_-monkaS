from flask import Flask
import sys

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Hi there, how ya doin?"

if __name__ == "__main__":
    app.run()
