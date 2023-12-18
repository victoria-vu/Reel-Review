"""Server for Reel Reviews app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud
import os
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.app_context().push()
API_KEY = os.environ["TMDB_API_KEY"]


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/search")
def search_movies():
    """Search for movies via TMDb API."""

    term = request.args.get("term")

    url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"
    payload = {
        "query": term
    }
    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }

    res = requests.get(url, params=payload, headers=headers)
    data = res.json()

    if "results" in data:
        movies = data["results"]
    else:
        movies = []

    total = len(movies)

    return render_template("all_movies.html", movies=movies, term=term, total=total)


@app.route("/movie/<movie_id>")
def show_movie(movie_id):
    """Show details about a particular movie."""

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
    "accept": "application/json",
    "Authorization": API_KEY
    }

    res = requests.get(url, headers=headers)
    movie = res.json()
    date_str = movie["release_date"]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%m/%d/%Y")

    return render_template("movie_details.html", movie=movie, formatted_date=formatted_date)


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/user/<user_id>")
def show_user(user_id):
    """Show details about a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/signup", methods=["POST"])
def signup_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")

    user = crud.get_user_by_email(email)

    if user:
        flash("A user with that email address already exists. Please try a different email address to register, or log in to your existing account.")
    else:
        user = crud.create_user(email, password, fname, lname)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been successfully created! Please log in.")

    return redirect("/login")


@app.route("/login")
def login_page():
    """View log in page."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_user():
    """Log in an existing user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user:
        flash("The email you typed in does not exist. Please sign up for an account or try again.")
    elif user:
        if password == user.password:
            session["user_id"] = user.user_id
            session["name"]= user.fname
            session["email"] = user.email
            flash("Logged in successfully.")
            return redirect("/")
        else:
            flash("Incorrect password. Please try again.")

    return redirect("/login")


@app.route("/logout")
def logout_user():
    """Log a user out of the session."""

    if "user_id" in session:
        session.clear()
        flash("You have signed out.")

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
