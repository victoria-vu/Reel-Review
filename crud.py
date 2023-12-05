""""CRUD Operations: Functions to create, retrieve, update, or delete data from the database."""

from model import db, User, Movie, Review, connect_to_db

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


def get_movie_by_id(movie_id):
    """Return a movie by movie id."""

    return Movie.query.get(movie_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)