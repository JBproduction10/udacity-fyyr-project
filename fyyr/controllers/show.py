from initApp import db
from model import Shows, Venue, Artist
from flask import render_template, request, Response, flash, redirect, url_for
from forms import *


def shows():
    # displays list of shows at /shows
    # completed: replace with real venues data.
    data = db.session.query(Shows).join(Artist).join(Venue).all()
    all_shows = []
    try:
        for show in data:
            all_shows.append({
                "venue_id": show.venue.id,
                "venue_name": show.venue.name,
                'artist_id': show.artist.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
            })
    except Exception as err:
        print(err)
        pass

    return render_template('pages/shows.html', shows=all_shows)


def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # completed: insert form data as a new Show record in the db, instead
    show_form = ShowForm()
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']

        show = Shows(artist_id=artist_id, venue_id=venue_id,
                     start_time=start_time)

        db.session.add(show)
        db.session.commit()
    # on successful db insert, flash success
        flash('Show was successfully listed!')
    # completed: on unsuccessful db insert, flash an error instead.
    except Exception as err:
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        db.session.rollback()
        flash("An error occurred. Show could not be listed.")
    finally:
        db.session.close()
    return render_template('pages/home.html')
