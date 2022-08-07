
from initApp import db
from model import Venue, Artist, Shows
from sqlalchemy import func
from flask import render_template, request, flash, redirect, url_for
from forms import *


def get_venues():
    # completed: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    venues = Venue.query.with_entities(func.count(
        Venue.id), Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
    data = []
    for area in venues:
        area_venues = Venue.query.filter_by(
            state=area.state).filter_by(city=area.city).all()
        venue_data = []
        for venue in area_venues:
            venue_data.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(db.session.query(Shows).filter(Shows.venue_id == 1).filter(Shows.start_time > datetime.now()).all())
            })
        data.append({
            "city": area.city,
            "state": area.state,
            "venues": venue_data
        })

    return render_template("pages/venues.html", areas=data)


def search_venues():
    # completed: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get("search_term", "")
    search_response = db.session.query(Venue).filter(
        Venue.name.ilike(f'%{search_term}%')).all()
    data = []
    for venue in search_response:
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(db.session.query(Shows).filter(Shows.venue_id == venue.id).filter(Shows.start_time > datetime.now()).all()),
        })
        print(data)

    response = {
        "count": len(search_response),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # completed: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)

    if not venue:
        return render_template('errors/404.html')

    upcoming_shows_query = db.session.query(Shows).join(Artist).filter(
        Shows.venue_id == venue_id).filter(Shows.start_time > datetime.now()).all()
    upcoming_shows = []

    past_shows_query = db.session.query(Shows).join(Artist).filter(
        Shows.venue_id == venue_id).filter(Shows.start_time < datetime.now()).all()
    past_shows = []

    for show in past_shows_query:
        past_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    for show in upcoming_shows_query:
        upcoming_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    data = {
        'id': venue.id,
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        "website_link": venue.website_link,
        'facebook_link': venue.facebook_link,
        'seeking_talent': venue.seeking_talent,
        'seeking_description': venue.seeking_description,
        'image_link': venue.image_link,
        'upcoming_shows': upcoming_shows,
        'upcoming_shows_count': len(upcoming_shows),
        'past_shows': past_shows,
        'past_shows_count': len(past_shows),
    }

    return render_template("pages/show_venue.html", venue=data)

# get venue create form


def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

# Create venue form


def create_venue_submission():
    venue_form = VenueForm()
    error = False
    try:
        # completed: insert form data as a new Venue record in the db, instead

        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        website_link = request.form['website_link']
        seeking_talent = True if 'seeking_talent' in request.form else False
        seeking_description = request.form['seeking_description']

        # completed: modify data to be the data object returned from db insertion
        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link,
                      image_link=image_link, website_link=website_link, seeking_talent=seeking_talent, seeking_description=seeking_description)
        db.session.add(venue)
        db.session.commit()
        flash(f'Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        error: True
        flash(f'An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        db.session.rollback()
        print(error)
    finally:
        db.session.close()
        # completed: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    return render_template('pages/home.html')


def delete_venue(venue_id):
    # completed: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    # error = False
    venue = Venue.query.filter_by(id=venue_id)
    try:
        # venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash('Venue {venue_id} was successfully deleted.')
    except:
        # error = True
        flash('An error occurred. Venue {venue_id} could not be deleted.')
        db.session.rollback()
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return render_template('pages/home.html')


def edit_venue(venue_id):
    form = VenueForm()
    # completed: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get(venue_id)

    if venue:
        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state
        form.phone.data = venue.phone
        form.address.data = venue.address
        form.genres.data = venue.genres
        form.facebook_link.data = venue.facebook_link
        form.image_link.data = venue.image_link
        form.website_link.data = venue.website_link
        form.seeking_talent.data = venue.seeking_talent
        form.seeking_description.data = venue.seeking_description
    return render_template('forms/edit_venue.html', form=form, venue=venue)


def edit_venue_submission(venue_id):
    error = False
    venue = Venue.query.get(venue_id)

    try:
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.genres = request.form.getlist('genres')
        venue.image_link = request.form['image_link']
        venue.facebook_link = request.form['facebook_link']
        venue.website = request.form['website']
        venue.seeking_talent = True if 'seeking_talent' in request.form else False
        venue.seeking_description = request.form['seeking_description']

        db.session.commit()
        flash('Venue was successfully updated!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue could not be changed.')
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))
