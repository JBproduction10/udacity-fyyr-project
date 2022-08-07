#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from sqlalchemy import func
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
# from model import db
from initApp import moment, db, migrate
from controllers import venue, show, artist

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# completed: implement any missing fields, as a database migration using Flask-Migrate
# Completed: implement any missing fields, as a database migration using Flask-Migrate
# completed Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


def register_initApp(app):
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app = Flask(__name__)
app.config.from_object('config')
register_initApp(app)


# completed: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    return venue.get_venues()


@app.route('/venues/search', methods=['POST'])
def search_venues():
    return venue.search_venues()


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    return venue.show_venue(venue_id)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    return venue.create_venue_form()


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    return venue.create_venue_submission()


@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    return venue.delete_venue(venue_id)

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    return artist.artists()


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # completed: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    return artist.search_artists()


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # completed: replace with real artist data from the artist table, using artist_id
    # artist_query = db.session.query(Artist).get(artist_id)
    return artist.show_artist(artist_id)
#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    # completed: populate form with fields from artist with ID <artist_id>
    return artist.edit_artist(artist_id)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # completed: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    return artist.edit_artist_submission(artist_id)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    return venue.edit_venue(venue_id)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    return venue.edit_venue_submission(venue_id)

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    return artist.create_artist_form()


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # completed: insert form data as a new Venue record in the db, instead
    return artist.create_artist_submission()


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    return artist.delete_artist(artist_id)

#  ----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # completed: replace with real venues data.
    return show.shows()


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    return show.create_shows()


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # completed: insert form data as a new Show record in the db, instead
    # # on successful db insert, flash success
    # # completed: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return show.create_show_submission()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:

if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=5000)
