# Project 1

### Dependencies
- flask_sqlalchemy
``` sudo pip install flask_sqlalchemy ```

## Oveview

A book review website with a database of 5000 books and the ability to take the book's isbn and use it as a GET request to Goodread's API

This project is aimed at buidling a lightweight web application that interfaces with a PostgreSQL database (Heroku in this case). I used the SQL Alchemy as the engine to lob raw SQL commands at the database. I also used JSONify for the json data from Goodreads 