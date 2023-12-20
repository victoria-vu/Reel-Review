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

    movie_in_db = crud.get_movie_by_id(movie_id)
    
    if movie_in_db:
        reviews = crud.get_all_movie_reviews(movie_id)
    else:
        reviews = []
    
    total_reviews = len(reviews)

    return render_template("movie_details.html", movie=movie, release_date=formatted_date, reviews=reviews, total_reviews=total_reviews)


@app.route("/addreview/<movie_id>", methods=["POST"])
def add_review(movie_id):
    """Create a review for a particular movie on movie details page.
    
    Two options:
    1. Create a new review.
    2. Update an existing review.
    *  A user can only have one review for a movie. *
    """

    movie_in_db = crud.get_movie_by_id(movie_id)

    # If movie is not in database, add into database.
    if not movie_in_db:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        headers = {
        "accept": "application/json",
        "Authorization": API_KEY
        }
        res = requests.get(url, headers=headers)
        movie = res.json()

        new_movie = crud.create_movie(
            movie_id,
            movie["original_title"],
            movie["overview"],
            movie["release_date"],
            movie["poster_path"]
        )
        db.session.add(new_movie)
        db.session.commit()
    
    movie = crud.get_movie_by_id(movie_id)
    rating = request.form.get("rating")
    review = request.form.get("review")
    user_id = session["user_id"]
    existing_review = crud.get_review_by_user_id(user_id)

    if not existing_review:
        new_review = crud.create_review(
            user_id,
            movie_id,
            rating,
            review
        )
        db.session.add(new_review)
        db.session.commit()
        flash(f"You have successfully created your review for {movie.title}.")
    
    elif existing_review:
        crud.update_review(existing_review, rating, review)
        flash(f"You have successfully updated your review for {movie.title}.")

    return redirect(f"/movie/{movie_id}")


@app.route("/myreviews")
def reviews_page():
    """View all user reviews."""

    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    reviews = crud.get_all_user_reviews(user_id)

    return render_template("user_reviews.html", user=user, reviews=reviews)


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