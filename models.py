from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def __str__(self):
        return f"{self.name} with id: {self.id}"

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship helper
    user = db.relationship("User", backref="movies")

    def __repr__(self):
        return '<Movie %r>' % self.title
    def __str__(self):
        return f"{self.title} with id: {self.id} and publication year: {self.year}"

