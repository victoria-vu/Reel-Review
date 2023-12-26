""""CRUD Operations: Functions to create, retrieve, update, or delete data from the database."""

from model import db, User, Movie, Review, connect_to_db
from flask import flash

### FUNCTIONS TO CREATE ###
def create_user(email, password, fname, lname):
    """Create and return a new user."""

    user = User(
        email=email,
        password=password,
        fname=fname,
        lname=lname
    )

    return user


def create_movie(id, title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(
        movie_id=id,
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=poster_path
    )

    return movie


def create_review(user_id, movie_id, rating, review):
    """Create and return a new review."""

    new_review = Review(
        user_id=user_id,
        movie_id=movie_id,
        rating=rating,
        review=review
    )

    return new_review


### FUNCTIONS TO RETRIEVE ###
def get_movies():
    """Return all movies from the database."""

    return Movie.query.all()


def get_all_movie_reviews(movie_id):
    """Return all reviews for a movie by movie id."""

    return Review.query.filter(Review.movie_id == movie_id).all()


def get_movie_by_id(movie_id):
    """Return a movie by movie id."""

    return Movie.query.get(movie_id)


def get_users():
    """Return all users from the database."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by user id."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def get_all_user_reviews(user_id):
    """Return all reviews for a user by user id."""

    return Review.query.filter(Review.user_id == user_id).all()


def get_review_by_user_id(user_id):
    """Return a review by user id."""

    return Review.query.filter(Review.user_id == user_id).first()


def get_review_by_review_id(review_id):
    """Return a review by review id."""

    return Review.query.filter(Review.review_id == review_id).first()


### FUNCTIONS TO UPDATE ###
def update_review(existing_review, new_rating, new_review):
    """Update an existing review for a user."""

    try:
        existing_review.rating = new_rating
        existing_review.review = new_review
        db.session.add(existing_review)
        db.session.commit()
    except Exception as e:
        flash("Sorry, we couldn't update your review.")
        print(e)


### FUNCTIONS TO DELETE ###
def delete_review(review_id):
    """Delete a review by review id."""

    review = get_review_by_review_id(review_id)
    db.session.delete(review)
    db.session.commit()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)