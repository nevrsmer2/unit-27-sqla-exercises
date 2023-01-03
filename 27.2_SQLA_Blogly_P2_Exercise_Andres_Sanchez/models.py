import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

now = datetime.datetime.utcnow


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
    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"

    """---------------PART 2--------------"""


class Post(db.Model):
    '''User Posts'''

    __tablename__ = 'posts'

    def __repr__(self):
        """Show info about users."""
        p = self
        return f'<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}>'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    title = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.String(1500), nullable=False)
    created_at = db.Column(db.DateTime, default=now,
                           onupdate=now, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    """---------------PART 2--------------"""


# ayawn = Post(title='Why kitties rock', content='Kitties rock because ...')
