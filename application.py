import os
import re

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
    # Get user input from login page
    newUsername = request.form.get("newUser")
    newPassword = request.form.get("newPass")

    # Check if user name exists
    if (db.execute("SELECT username FROM users WHERE username = :username", {"username": newUsername}).rowcount == 1):
        return render_template("error.html", message="Username already exists")

    # Check for little Bobby Drop Tables
    if re.search("[']", newPassword):
        return render_template("error.html", message="Invalid Password")

    #Insert into database - the password is stored in the data base encrypted for security
    db.execute("INSERT INTO users (username, password) VALUES (:username, crypt(:password, gen_salt('bf')))",
                {"username": newUsername, "password": newPassword})
    db.commit()
    
    return render_template("success.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/verify", methods=["POST", "GET"])
def verify():
    user = request.form.get("existingUser")
    xpass = request.form.get("existingPass")

    #check for user in user table
    if db.execute("SELECT id FROM users WHERE username = :username AND password = crypt(:password, password);", {"username": user, "password": xpass}).rowcount == 1:
        return render_template("error.html", message="Invalid username/password")
    else:
        return render_template("main.html")

@app.route("/success", methods=["POST"])
def success():
    return render_template("success.html")

@app.route("/main")
def main():
    return render_template("main.html")



