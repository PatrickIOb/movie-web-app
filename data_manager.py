from models import db, User, Movie

class DataManager():

    def create_user(self, name):
        """create a new user"""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        """gets all users"""
        return User.query.all()

    def get_movies(self, user_id):
        """gets all the movies associated with the user"""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """adds a movie to the database"""
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """updates a movie from the database"""
        movie = Movie.query.get(movie_id)
        if movie:
            movie.title = new_title
            db.session.commit()
            return movie
        return None


    def delete_movie(self, movie_id):
        """deletes a movie from the database"""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False

