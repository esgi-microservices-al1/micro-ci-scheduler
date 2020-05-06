from flask import Flask
from dbconnection import db
import pymongo

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == '__main__':
    app.run()