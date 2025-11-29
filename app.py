from flask import Flask, redirect, render_template, request, url_for
from data_manager import DataManager
from dotenv import load_dotenv
from models import db, User, Movie
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager()

@app.route('/', methods=['GET'])
def index():
    """show a list of all registered users and a form to add a new user"""
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route('/users', methods=['POST'])
def add_user():
    """handle form to add new user and then redirect to homepage"""
    name = request.form['name']  # the form field will be called 'name'
    data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def movies(user_id):
    """show a list of movies for a user (GET) and add a new movie (POST)"""
    if request.method == "POST":
        title = request.form['title']
        year = request.form.get('year')

        # convert year to int or None
        if year:
            try:
                year = int(year)
            except ValueError:
                year = None

        new_movie = Movie(title=title, year=year, user_id=user_id)
        data_manager.add_movie(new_movie)

        # Post/Redirect/Get pattern
        return redirect(url_for('movies', user_id=user_id))

    user = User.query.get_or_404(user_id)
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", user=user, movies=movies)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """update a movie title for a user"""
    new_title = request.form['title']
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """delete a movie from a user's list"""
    data_manager.delete_movie(movie_id)
    return redirect(url_for('movies', user_id=user_id))


if __name__ == '__main__':
    #uncomment and run once
    """with app.app_context():
    db.create_all()"""
    app.run()

