from streamapp import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# class User(db.Model, UserMixin):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     created_at = db.Column(db.DateTime,  nullable=False,
#                            default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime,  nullable=False,
#                            default=datetime.utcnow, onupdate=datetime.utcnow)
#     deleted_at = db.Column(db.DateTime,  nullable=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), unique=True, nullable=False)
    

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    
class UserExperience(db.Model, UserMixin):
    __tablename__ = 'userexperience'
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))
    scrobbles = db.Column(db.Integer)
 
class Artist(db.Model, UserMixin):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User, foreign_keys=user_id)    

class Album(db.Model, UserMixin):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
    artist = db.relationship(Artist, foreign_keys=artist_id)

class Track(db.Model, UserMixin):
    __tablename__ = 'tracks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey(Album.id))
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
    artist = db.relationship(Artist, foreign_keys=artist_id)
    album = db.relationship(Album, foreign_keys=album_id)
    
# class Artist(db.Model, UserMixin):
#     __tablename__ = 'artists'
#     id = db.Column(db.Integer, primary_key=True)
#     created_at = db.Column(db.DateTime,  nullable=False,
#                            default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime,  nullable=False,
#                            default=datetime.utcnow, onupdate=datetime.utcnow)
#     deleted_at = db.Column(db.DateTime,  nullable=True)
#     name = db.Column(db.String(250), nullable=False)
#     country = db.Column(db.String(250), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey(User.id))
#     user = db.relationship(User, foreign_keys=user_id)
    

# class Album(db.Model, UserMixin):
#     __tablename__ = 'albums'
#     id = db.Column(db.Integer, primary_key=True)
#     created_at = db.Column(db.DateTime,  nullable=False,
#                            default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime,  nullable=False,
#                            default=datetime.utcnow, onupdate=datetime.utcnow)
#     deleted_at = db.Column(db.DateTime,  nullable=True)
#     name = db.Column(db.String(250), nullable=False)
#     duration = db.Column(db.String(250), nullable=False)
#     artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
#     artist = db.relationship(Artist, foreign_keys=artist_id)
     
     
# class Track(db.Model, UserMixin):
#     __tablename__ = 'tracks'
#     id = db.Column(db.Integer, primary_key=True)
#     created_at = db.Column(db.DateTime,  nullable=False,
#                            default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime,  nullable=False,
#                            default=datetime.utcnow, onupdate=datetime.utcnow)
#     deleted_at = db.Column(db.DateTime,  nullable=True)
#     name = db.Column(db.String(250), nullable=False)
#     duration = db.Column(db.String(250), nullable=False)
#     genre = db.Column(db.String(250), nullable=False)
#     rating = db.Column(db.String(250), nullable=False)
#     artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
#     album_id = db.Column(db.Integer, db.ForeignKey(Album.id))
#     artist = db.relationship(Artist, foreign_keys=artist_id)
#     album = db.relationship(Album, foreign_keys=album_id)
    
    
    
    
    