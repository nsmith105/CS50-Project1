import os, re
from models import *

from flask import session, render_template, request, redirect, jsonify
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
    ### User name successfully added to DB ###
    return render_template("success.html")

@app.route("/main")
def main():
    ### Main landing page ###
    return render_template("main.html")

@app.route("/results", methods=["GET", "POST"])
def results():
    ### Search results pages ###
    results = request.form.get("searchinfo")
    results = '%' + results + '%'

    if db.execute("SELECT * FROM books WHERE isbn LIKE :result OR lower(author) LIKE lower(:result) OR lower(title) LIKE lower(:result);", {"result": results}).rowcount == 0:
        return render_template ("error.html", message="Your search returned no results, please try agian!")
    bookinfo = db.execute("SELECT * FROM books WHERE isbn LIKE :result OR lower(author) LIKE lower(:result) OR lower(title) LIKE lower(:result);", {"result": results}).fetchall()
    return render_template("results.html", bookinfo=bookinfo)

@app.route("/books")
def books():
    allbooks = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", allbooks=allbooks)


@app.route("/books/<string:isbn>")
def book(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :book_isbn", {"book_isbn": isbn} ).fetchone()
    if book is None:
        return render_template("error.html", message="That book is not in our database")
    
    return render_template("book.html", book=book)

@app.route("/api/books/<string:isbn>", methods=["GET"])
def book_api(isbn):
    book_info = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": DCM6bTHII2EmK8RWecMPWA, "isbn": isbn})
    if book_info is None:
        return jsonify({"error": "Invalid flight_id"}), 422
    return jsonify({
            "title": book_info.title,
            "author": book_info.author,
            "year": book_info.year,
            "isbn": book_info.isbn,
            "reviews": book_info.review_count,
            "average score": book_info.average_score
        })


