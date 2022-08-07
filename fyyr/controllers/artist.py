from model import Shows, Venue, Artist
from initApp import db
from sqlalchemy import func
from flask import render_template, request, Response, flash, redirect, url_for
from forms import *


def artists():
    artists = db.session.query(Artist).all()

    return render_template('pages/artists.html', artists=artists)


def search_artists():
    # completed: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get("search_term", '')
    search_response = db.session.query(Artist).filter(
        Artist.name.ilike(f'%{search_term}%')).all()
    data = []
    for artist in search_response:
        data.append({
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows': len(db.session.query(Shows).filter(Shows.artist_id == artist.id).filter(Shows.start_time > datetime.now()).all()),
        })
    response = {
        "count": len(search_response),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # completed: replace with real artist data from the artist table, using artist_id
    artist_query = Artist.query.get(artist_id)
    if not artist_query:
        return render_template('errors/404.html')

    past_shows_query = db.session.query(Shows).join(Venue).filter(
        Shows.artist_id == artist_id).filter(Shows.start_time > datetime.now()).all()
    past_shows = []

    for show in past_shows_query:
        past_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_image_link": show.venue.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    upcoming_shows_query = db.session.query(Shows).join(Venue).filter(
        Shows.artist_id == artist_id).filter(Shows.start_time > datetime.now()).all()
    upcoming_shows = []

    for show in upcoming_shows_query:
        upcoming_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_image_link": show.venue.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    data = {
        "id": artist_query.id,
        "name": artist_query.name,
        'genres': artist_query.genres,
        'city': artist_query.city,
        'state': artist_query.state,
        'phone': artist_query.phone,
        "website_link": artist_query.website_link,
        'facebook_link': artist_query.facebook_link,
        'image_link': artist_query.image_link,
        'seeking_venue': artist_query.seeking_venue,
        'seeking_description': artist_query.seeking_description,
        'upcoming_shows_count': len(upcoming_shows),
        'upcoming_shows': upcoming_shows,
        'past_shows': past_shows,
        'past_shows_count': len(past_shows)
    }
    return render_template('pages/show_artist.html', artist=data)


def edit_artist(artist_id):
    form = ArtistForm()
    # completed: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.filter_by(id=artist_id).first()

    if artist:
        form.name.data = artist.name
        form.city.data = artist.city
        form.state.data = artist.state
        form.phone.data = artist.phone
        form.genres.data = artist.genres
        form.facebook_link.data = artist.facebook_link
        form.image_link.data = artist.image_link
        form.website_link.data = artist.website_link
        form.seeking_venue.data = artist.seeking_venue
        form.seeking_description.data = artist.seeking_description
    return render_template('forms/edit_artist.html', form=form, artist=artist)


def edit_artist_submission(artist_id):
    # completed: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm()

    artist = Artist.query.get(artist_id)
    try:
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.genres = request.form.getlist('genres')
        artist.image_link = request.form['image_link']
        artist.facebook_link = request.form['facebook_link']
        artist.website_link = request.form['website_link']
        artist.seeking_venue = True if 'seeking_venue' in request.form else False
        artist.seeking_description = request.form['seeking_description']

        db.session.add(artist)
        db.session.commit()
        flash('Artist was successfully updated!')
    except Exception as err:
        db.session.rollback()
        flash('An error occurred. Artist could not be changed.')
    return redirect(url_for('show_artist', artist_id=artist_id))


def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


def create_artist_submission():
    # called upon submitting the new artist listing form
    # completed: insert form data as a new Venue record in the db, instead
    form = ArtistForm()
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        facebook_link = request.form['facebook_link']
        image_link = request.form['image_link']
        website_link = request.form['website_link']
        seeking_venue = True if 'seeking_venue' in request.form else False
        seeking_description = request.form['seeking_description']

        artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link,
                        image_link=image_link, website_link=website_link, seeking_venue=seeking_venue, seeking_description=seeking_description)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as err:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


def delete_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id)
    try:
        db.session.delete(artist)
        db.session.commit()
        flash("Artist {artist_id} was successfully deleted.")
    except Exception as err:
        flash('An error occurred. Artist {artist_id} could not be deleted.')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template("pages/home.html")
