import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = "books"
    isbn =      db.Column(db.String, primary_key=True)
    author =    db.Column(db.String, nullable=False)
    title =     db.Column(db.String, nullable=False)
    date =      db.Column(db.String, nullable=False)
    reviews =   db.relationship("Review", backref="book", lazy=True)

    def add_review(sel rating, note):
        r = Review(rating = rating, note = note isbn=self.isbn)
        db.session.add(r)
        db.session.commit()

class Review(db.Model):
    __table__ = "reviews"
    rating =    db.Column(db.Integer, nullable=False)
    note =      db.Column(db.String, nullable=True)
    book_isbn = db.column(db.String, primary_key=True, db.ForeignKey("books.isbn"), nullable=False)