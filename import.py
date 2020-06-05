import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

f = open("books.csv")
reader = csv.reader(f)
db.execute("CREATE TABLE books (isbn VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, author VARCHAR NOT NULL, date VARCHAR NOT NULL);")
for isbn, title, author, date in reader:
    db.execute("INSERT INTO books (isbn, title, author, date) VALUES (:isbn, :title, :author, :date)", 
                {"isbn": isbn, "title": title, "author": author, "date": date})
    print(f"Added: {title} from {author} - {date} - {isbn}")
db.commit()



