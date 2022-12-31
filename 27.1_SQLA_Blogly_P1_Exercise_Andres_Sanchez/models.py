from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

    """---------------Models for Blogly---------------"""


class User(db.Model):
    """User Class"""

    __tablename__ = "users"

    def __repr__(self):
        """Show info about users."""
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(15),
                           nullable=False)

    last_name = db.Column(db.String(15),
                          nullable=False)
    image_url = db.Column(db.String(100),
                          nullable=True)

    """---------------Instance Methods--------------"""
