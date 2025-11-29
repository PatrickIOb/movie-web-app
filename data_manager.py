from models import db, User, Movie

class DataManager():

    def create_user(self, name):
        """create a new user"""
        new_user = User(name=name)
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            print("Database error while creating user:", e)
            return None


    def get_users(self):
        """gets all users"""
        return User.query.all()


    def get_movies(self, user_id):
        """gets all the movies associated with the user"""
        return Movie.query.filter_by(user_id=user_id).all()


    def add_movie(self, movie):
        """adds a movie to the database safely"""
        try:
            db.session.add(movie)
            db.session.commit()
            return movie
        except Exception as e:
            db.session.rollback()
            print("Database error while adding movie:", e)
            return None


    def update_movie(self, movie_id, new_title):
        """updates a movie from the database"""
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                print(f"Movie with id {movie_id} not found.")
                return None

            movie.title = new_title
            db.session.commit()
            return movie
        except Exception as e:
            db.session.rollback()
            print("Database error while updating movie:", e)
            return None


    def delete_movie(self, movie_id):
        """deletes a movie from the database"""
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                print(f"Movie with id {movie_id} not found.")
                return False

            db.session.delete(movie)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print("Database error while deleting movie:", e)
            return False
