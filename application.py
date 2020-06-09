import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["POST", "GET"])
def create():
    newUsername = request.form.get("newUser")
    newPassword = request.form.get("newPass")
    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                {"username": newUsername, "password": newPassword})
    db.commit()
    return render_template("success.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/success", methods=["POST"])
def success():
    return render_template("success.html")

@app.route("/main")
def main():
    return render_template("main.html")



