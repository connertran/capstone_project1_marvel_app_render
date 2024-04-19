import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt= Bcrypt()

def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()


#models go below here
class User(db.Model):
    """User model."""
    __tablename__ = "users"

    username = db.Column(db.Text,
                         primary_key=True,
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                           nullable=False)
    bio = db.Column(db.Text,
                    nullable=False)
    password = db.Column(db.Text,
                         nullable=False)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    favorite_characters = db.relationship("FavoriteCharacters", backref= "user", cascade="all, delete-orphan")
    likes = db.relationship("Like", backref="user", cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="user", cascade="all, delete-orphan")

    def greet(self):
        return f"username: {self.username}; email: {self.email}; first_name: {self.first_name}; last_name: {self.last_name}"
    
    def serialize(self):
        return {
            'username': self.username,
            'email': self.email,
            'image_url': self.image_url,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'bio': self.bio
        }
    @classmethod
    def register(cls, user_password):
        """Register user with hashed password & return hashed password"""
        hashed = bcrypt.generate_password_hash(user_password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return hashed password
        return cls(password = hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """validate that user exists & passord is correct
        Return user if valid; else return False"""
        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            #return user instance
            return u
        else:
            return False

    
class Post(db.Model):
    """Post model."""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key =True,
                   autoincrement=True)
    text = db.Column(db.Text,
                    nullable=False)
    timestamp = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.datetime.now)
    user_id = db.Column(db.Text, 
                        db.ForeignKey('users.username', ondelete="cascade"), 
                        nullable=False)

    likes = db.relationship("Like", backref="post", cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan")

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.timestamp.strftime("%a %b %-d  %Y, %-I:%M %p")

class Like(db.Model):
    """Post Like model."""
    __tablename__ = "likes"

    id = db.Column(db.Integer,
                   primary_key =True,
                   autoincrement=True)
    user_id = db.Column(db.Text, db.ForeignKey('users.username', ondelete="cascade"), 
                        nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="cascade"), 
                        nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id}
class Comment (db.Model):
    """Post comment model."""
    __tablename__ = "comments"

    id = db.Column(db.Integer,
                   primary_key =True,
                   autoincrement=True)
    text = db.Column(db.Text,
                    nullable=False)
    user_id = db.Column(db.Text, db.ForeignKey('users.username', ondelete="cascade"), 
                        nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="cascade"), 
                        nullable=False)
    timestamp = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.datetime.now)
    
    def serialize(self):
        return {
            'id': self.id,
            'text': self.text,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'timestamp': self.timestamp
        }
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.timestamp.strftime("%a %b %-d  %Y, %-I:%M %p")
    
class MarvelCharacters(db.Model):
    """Marvel characters from Marvel API model"""
    __tablename__ = "characters"

    # the id fetched from Marvel API
    id = db.Column(db.Integer,
                   primary_key =True)
    name = db.Column(db.Text,
                     nullable=False)
    thumbnail = db.Column(db.Text,
                          nullable=False,
                          default='https://i.pinimg.com/564x/f8/34/20/f834200e7e42ea53b4fba62a17c8f107.jpg')
    description = db.Column(db.Text,
                            nullable=False,
                            default='No description')
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)

    favorite_characters = db.relationship("FavoriteCharacters", backref= "character", cascade="all, delete-orphan")
    comics_characters = db.relationship("ComicsCharacters", backref= "character", cascade="all, delete-orphan")
    comics = db.relationship("MarvelComics", secondary = "comics_characters", backref="characters")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'thumbnail': self.thumbnail,
            'description': self.description,
            'created_at': self.created_at
        }
class MarvelComics(db.Model):
    """Marvel comics from Marvel API model"""
    __tablename__ = "comics"

    id = db.Column(db.Integer,
                   primary_key =True)
    title = db.Column(db.Text,
                     nullable=False)
    comics_characters = db.relationship("ComicsCharacters", backref= "comics", cascade="all, delete-orphan")
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'comics_characters': self.description,
            'created_at': self.created_at
        }
class ComicsCharacters(db.Model):
    """Association table for characters and comics model."""
    __tablename__="comics_characters"

    id = db.Column(db.Integer,
                   primary_key =True,
                   autoincrement=True)
    character_id = db.Column(db.Integer, 
                             db.ForeignKey('characters.id', ondelete="cascade"),
                             nullable=False)
    comics_id = db.Column(db.Integer, 
                             db.ForeignKey('comics.id', ondelete="cascade"),
                             nullable=False)
    
class FavoriteCharacters(db.Model):
    """User's favorite characters model."""
    __tablename__="favorite_characters"

    id = db.Column(db.Integer,
                   primary_key =True,
                   autoincrement=True)
    user_id = db.Column(db.String, 
                              db.ForeignKey('users.username', ondelete="cascade"), 
                              nullable=False)
    character_id = db.Column(db.Integer, 
                             db.ForeignKey('characters.id', ondelete="cascade"),
                             nullable=False)
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'character_id': self.character_id
        }
    