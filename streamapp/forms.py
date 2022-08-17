from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL, ValidationError
from streamapp.models import Artist, User, Album
#from streamapp.routes import search
             
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])   
    submit = SubmitField('Sign Up') 
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    
   
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Oppa'), Email()])
    password = PasswordField('Password', validators=[DataRequired('Oppala')]) 
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
    
class ArtistForm(FlaskForm):
    artist_name = StringField('Artisi Name', validators=[DataRequired('Oppala')]) 
    country_of_origin = StringField('Country of origin', validators=[DataRequired('Oppala')])  
    submit = SubmitField('Save')
    
class AlbumForm(FlaskForm): 
    album_title = StringField('Album title', validators=[DataRequired('Oppala')]) 
    artist = SelectField('Main artist', validators=[DataRequired()])
    # def __init__(self, *args, **kwargs):
    #     super(AlbumForm, self).__init__(*args, **kwargs)
    #     self.artist.choices = [(g.id, g.name) for g in Artist.query.all()]
    album_duration = StringField('Album duration', validators=[DataRequired()])
    submit = SubmitField('Save')
    
class TracksForm(FlaskForm): 
    track_name = StringField('Track name', validators=[DataRequired('Oppala')]) 
    artist = SelectField('Main artist', validators=[DataRequired()], default=0) 
    album = SelectField('Album name', default=0)   
    track_duration = StringField('Track duration', validators=[DataRequired()])
    genre_id = StringField('Track genre', validators=[DataRequired()])
    rating = StringField('Track rating', validators=[DataRequired()])
    submit = SubmitField('Save')
               
class SearchForm(FlaskForm): 
    name = StringField('Artist, album or track name', validators=[DataRequired('Oppala')])     
    submit = SubmitField('Search')
    
