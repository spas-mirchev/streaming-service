from email.policy import default
from flask import render_template, redirect, flash, url_for, request, session
from streamapp.models import UserExperience, User, Artist, Album, Track
from streamapp import app
from streamapp import db
from streamapp.forms import RegistrationForm, LoginForm, ArtistForm, AlbumForm, SearchForm, TracksForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
import re
import numpy as np
from scipy import sparse
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

# db.create_all()


class NotFoundException(Exception):
    pass


class NotLoggedInException(Exception):
    pass


@app.route("/", methods=['GET', 'POST'])
def home():
    ind_col = np.array([a.user_id for a in UserExperience.query.all()])
    artist_col = np.array([a.artist_id for a in UserExperience.query.all()])
    scrobbles_col = np.array([a.scrobbles for a in UserExperience.query.all()])
    
    titles_dict = {a.id:a.name for a in Artist.query.all()}
    
   
    
    rows, r_pos = np.unique(ind_col, return_inverse=True)
    cols, c_pos = np.unique(artist_col, return_inverse=True)

    interactions_sparse = sparse.csr_matrix(
         (scrobbles_col, (r_pos, c_pos)))

    Pui = normalize(interactions_sparse, norm='l2', axis=0)
    sim = Pui.T * Pui

    sim_artists = [titles_dict[i+1]
               for i in sim[13303].toarray().argsort()[0][-20:]]
    
    fit = Pui * Pui.T * Pui
    
    predicted_set = [titles_dict[i+1] for i in fit[2].toarray().argsort()[0][-70:].tolist()]
    
    recommended_tracks = Track.query.all()[:4]
    recommended_albums = Album.query.all()[:4]

    return render_template("index.html", recommended_albums=recommended_albums, recommended_tracks=recommended_tracks,  logged_in=current_user.is_authenticated, Pui=Pui, predicted_set=predicted_set)


@app.route("/player/<int:track_id>", methods=['GET', 'POST'])
def player(track_id):

    recommended_tracks = Track.query.all()
    played_track = f"/static/music/t{track_id}.mp3"

    tracks_row = Track.query.filter_by(id=track_id).first()
    # if not tracks_row:
    #     raise NotFoundException()
    user_experience = UserExperience.query.filter_by(
        user_id=current_user.id, artist_id=tracks_row.artist_id).first()
    if not user_experience:
        user_experience = UserExperience(
            user_id=current_user.id, artist_id=tracks_row.artist_id, scrobbles=1)
        db.session.add(user_experience)
    else:
        user_experience.scrobbles += 1

    db.session.commit()
    flash(f'Evala {current_user.username}', 'warning')

    return render_template("index.html", played_track=played_track, recommended_tracks=recommended_tracks,  logged_in=current_user.is_authenticated)


@app.route("/publisher", methods=['GET', 'POST'])
def publisher():
    args = request.args
    artist_id = args.get('artist_id')
    album_id = args.get('album_id')
    track_id = args.get('track_id')

    user_artists = Artist.query.filter_by(user_id=current_user.id).all()

    user_albums_all = [Album.query.filter_by(
        artist_id=artist.id).all() for artist in user_artists]
    user_albums = [j for sub in user_albums_all for j in sub]

    user_tracks_all = [Track.query.filter_by(
        artist_id=artist.id).all() for artist in user_artists]
    user_tracks = [j for sub in user_tracks_all for j in sub]

    form_artists = ArtistForm()
    form_albums = AlbumForm()
    form_tracks = TracksForm()

    if form_artists.validate_on_submit():
        artist = Artist(name=form_artists.artist_name.data,
                        country=form_artists.country_of_origin.data, user_id=current_user.id)
        db.session.add(artist)
        db.session.commit()
        flash(f'Welcome {artist.name}', 'warning')

    if album_id:
        form_albums.artist.choices = [
            (artist.id, artist.name) for artist in user_artists]
        if form_albums.validate_on_submit():
            artist_id = Artist.query.filter_by(
                id=form_albums.artist.data).first().id
            album = Album(name=form_albums.album_title.data,
                          artist_id=artist_id, duration=form_albums.album_duration.data)

            db.session.add(album)
            db.session.commit()
            flash(f'Evala {album.artist.name}', 'warning')

    if track_id:

        form_tracks.artist.choices = [
            (artist.id, artist.name) for artist in user_artists]
        form_tracks.album.choices = [(album.id, album.name) for album in user_albums]
        
        if form_tracks.validate_on_submit():
            album_id = Album.query.filter_by(id=form_tracks.album.data).first().id
            artist_id = Artist.query.filter_by(id=form_tracks.artist.data).first().id
            track = Track(name=form_tracks.track_name.data, album_id= album_id, artist_id=artist_id)
            db.session.add(track)
            db.session.commit()
            flash(f'Evala {album.artist.name}', 'warning')
       
    return render_template("publisher.html", current_user=current_user, user_artists=user_artists, user_albums=user_albums, user_tracks=user_tracks) 

@app.route("/search", methods=['GET', 'POST'])
def search():
    
    return render_template("search.html")

                                     
@app.route("/register", methods=['GET', 'POST'])  
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        user = User(username=form.username.data,
                     email=form.email.data, password=hash_and_salted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {user.username} !', 'info')
        login_user(user)
        return redirect(url_for('home'))
    return render_template("register.html", title='Register', form=form, logged_in=current_user.is_authenticated)                                   

@app.route("/login", methods=['GET', 'POST'])  
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.", 'warning')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Invalid password provided', 'warning')
            return redirect(url_for('login'))
        else:
            login_user(user)
            flash(f'Hi {current_user.username}!', 'success')
            return redirect(url_for('home'))

    return render_template("login.html", title='Login', form=form, logged_in=current_user.is_authenticated)  

@app.route("/logout") 
@login_required 
def logout():
    logout_user()
    flash('You logged out', 'info')
    return redirect(url_for('home'))