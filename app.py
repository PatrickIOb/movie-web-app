from flask import flash, Flask, redirect, render_template, request, url_for
from data_manager import DataManager
from dotenv import load_dotenv
from models import db, User, Movie
import os
import requests

load_dotenv()
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()

def fetch_movie_from_omdb(title, year=None):
    """
    Call OMDb API with a title (and optional year).
    Safely handles connection errors and missing data.
    """
    try:
        params = {
            "t": title,
            "apikey": API_KEY
        }
        if year:
            params["y"] = year

        resp = requests.get("https://www.omdbapi.com/", params=params, timeout=5)
        data = resp.json()

        if data.get("Response") == "False":
            return None

        # Safely parse year
        parsed_year = None
        if data.get("Year") and data["Year"].isdigit():
            parsed_year = int(data["Year"])

        poster = data.get("Poster")
        if not poster or poster == "N/A":
            poster = None

        return {
            "title": data.get("Title") or title,
            "year": parsed_year,
            "director": data.get("Director"),
            "poster_url": poster,
        }

    except requests.exceptions.RequestException as e:
        # Network errors or timeouts
        print("OMDb API error:", e)
        return None

    except Exception as e:
        # Unexpected errors (wrong JSON, etc.)
        print("Unexpected OMDb error:", e)
        return None

@app.route('/', methods=['GET'])
def index():
    """show a list of all registered users and a form to add a new user"""
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route('/users', methods=['POST'])
def add_user():
    """handle form to add new user and then redirect to homepage"""
    name = request.form['name']
    data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def movies(user_id):
    """show a list of movies for a user (GET) and add a new movie (POST)"""
    if request.method == "POST":
        raw_title = request.form['title']
        year_input = request.form.get('year')

        year = None
        if year_input:
            try:
                year = int(year_input)
            except ValueError:
                year = None

        # Fetch info from OMDb
        movie_data = fetch_movie_from_omdb(raw_title, year)

        # Fallback if OMDb returns nothing
        if not movie_data:
            flash("Could not fetch details from OMDb. Saved basic title only.", "warning")
            movie_data = {
                "title": raw_title,
                "year": year,
                "director": None,
                "poster_url": None,
            }
        else:
            flash("Movie details fetched from OMDb and saved.", "success")

        new_movie = Movie(
            title=movie_data["title"],
            year=movie_data["year"],
            director=movie_data["director"],
            poster_url=movie_data["poster_url"],
            user_id=user_id,
        )

        saved = data_manager.add_movie(new_movie)
        if saved is None:
            flash("There was a problem saving the movie to the database.", "error")


        return redirect(url_for('movies', user_id=user_id))

    user = User.query.get_or_404(user_id)
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", user=user, movies=movies)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """update a movie title for a user"""
    new_title = request.form['title']
    updated = data_manager.update_movie(movie_id, new_title)

    if updated:
        flash("Movie updated successfully.", "success")
    else:
        flash("Could not update movie.", "error")

    return redirect(url_for('movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """delete a movie from a user's list"""
    success = data_manager.delete_movie(movie_id)

    if success:
        flash("Movie deleted.", "success")
    else:
        flash("Could not delete movie.", "error")

    return redirect(url_for('movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    #uncomment and run once
    """with app.app_context():
        db.create_all()"""
    app.run()

