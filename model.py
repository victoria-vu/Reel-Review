"""Models for Reel Reviews app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    reviews = db.relationship("Review", back_populates="user")

    def __repr__(self):
        """Return user id, name, and email of a User object."""

        return f"<User user_id={self.user_id} name={self.fname} email={self.email}>"
    

class Movie(db.Model):
    """A movie."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    overview = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    poster_path = db.Column(db.String, nullable=True)

    reviews = db.relationship("Review", back_populates="movie")

    def __repr__(self):
        """Return movie id and title of a Movie object."""

        return f"<Movie movie_id={self.movie_id} title={self.title}>"
    

class Review(db.Model):
    """A movie review."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=True)
    review_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    movie = db.relationship("Movie", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        """Return review id and rating of a Review object."""

        return f"<Review review_id={self.review_id} rating={self.rating}>"
    

def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)