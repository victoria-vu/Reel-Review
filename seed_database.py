"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# Automate the process of creating the database.
os.system("dropdb ratings")
os.system("createdb ratings")
model.connect_to_db(server.app)
model.db.create_all()

with open("data/movies.json") as f:
    movie_data = json.loads(f.read())

# Automate the process of populating the database.
movies_in_db = []
for movie in movie_data:
    id, title, overview, poster_path = (
        movie["id"],
        movie["original_title"],
        movie["overview"],
        movie["poster_path"]
    )

    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    db_movie = crud.create_movie(id, title, overview, release_date, poster_path) 
    movies_in_db.append(db_movie) 

model.db.session.add_all(movies_in_db)
model.db.session.commit()

# Automate the process of adding fake users.
fake_users_in_db = []
for n in range(10):
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(email, password, f"User{n}", f"User{n}")
    fake_users_in_db.append(user)

model.db.session.add_all(fake_users_in_db)
model.db.session.commit()