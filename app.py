#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.policy import default
#import json
import dateutil.parser
import babel
#from django.dispatch import receiver
from flask import (
  Flask, 
  render_template, 
  request,
  Response, 
  flash, 
  redirect, 
  url_for, 
  jsonify
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
import sys
from model import *
from forms import facebook
#-------------ss---------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
Migrate(app, db)

# TODO: connect to a local postgresql database

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  test_data = Venue.query.all()
  states = set()
  data = []
  for i in test_data:
    states.add(i.state)
  counter = 0
  for state in states:
    state_data = Venue.query.filter_by(state=state).all()
    city_data = {}
    for info in state_data:
      city = info.city
      if city.lower() not in city_data:
        data.append({})
        data[counter]['city'] = city
        city_data[city.lower()] = len(data) - 1
        data[counter]['state'] = info.state
        data[counter]['venues'] = []
        data[counter]['venues'].append({
              "id": info.id,
              "name": info.name,
              "num_upcoming_shows": upcoming(info, 'Venue')[0]
            })
        counter += 1
      else:
        data[city_data[city.lower()]]['venues'].append({
              "id": info.id,
              "name": info.name,
              "num_upcoming_shows": upcoming(info, 'Venue')[0]
            })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  response = {'count': 0, 'data': []}
  if search_term != '':
    db_response = Venue.query.filter(Venue.name.ilike("%" + search_term + "%"))
    for i in db_response:
      response['count'] += 1
      response['data'].append({
        "id": i.id,
        "name": i.name,
        "num_upcoming_shows": upcoming(i, 'Venue')[0]
      })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter_by(id=venue_id).first()
  #show = Show.query.filter_by(venue_id=venue_id)
  upcoming_show = upcoming(venue, 'Venue')
  past_show = past(venue, 'Venue')
  data = {
    "id": venue_id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": past_show[0],
    "upcoming_shows_count": upcoming_show[0],
  }
  for i in past_show[1]:
    artist = Artist.query.filter_by(id=i.artist_id).first()
    data['past_shows'].append({
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(i.start_time)
    })
  for i in upcoming_show[1]:
    artist = Artist.query.filter_by(id=i.artist_id).first()
    data['upcoming_shows'].append({
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(i.start_time)
    })
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate_on_submit():
    print("Here")
    try:
      # TODO: insert form data as a new Venue record in the db, instead
      #Gets each item from form and adds it to data with its data type in the database
      # TODO: modify data to be the data object returned from db insertion
      #insert data into db
      venue = Venue(
        city=form.city.data, 
        name=form.name.data, 
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website_link=form.website_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data
      )
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + form.name.data + ' was successfully listed!')
      #try_except(venue, "Venue ", form.name.data, form.name.data)
      # on successful db insert, flash success
      #flash('Venue ' + form'name'] + ' was successfully listed!')
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    except:
      db.session.rollback()
      flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  else:
    if not facebook(request.form['facebook_link']):
      flash("Ensure your link is of the form https://www.facebook.com/")
    else:
      flash('Invalid_form. Please try again')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    Show.query.filter_by(venue_id=venue_id).delete()
    db.session.commit()
    value = True
  except:
    db.session.rollback()
    value = False
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  print('for')
  return jsonify({'value': value})
  #return redirect(url_for('index', _method="GET"))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[]
  artists = Artist.query.all()
  for i in artists:
    data.append({
      "id": i.id,
      "name" : i.name
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')
  response = {'count': 0, 'data': []}
  if search_term != '':
    db_response = Artist.query.filter(Artist.name.ilike("%" + search_term + "%"))
    for i in db_response:
      response['count'] += 1
      response['data'].append({
        "id": i.id,
        "name": i.name,
        "num_upcoming_shows": upcoming(i, 'Artist')[0]
      })
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.filter_by(id=artist_id).first()
  #show = Show.query.filter_by(venue_id=artist_id)
  upcoming_show = upcoming(artist, 'Artist')
  past_show = past(artist, 'Artist')
  data = {
    "id": artist_id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": past_show[0],
    "upcoming_shows_count": upcoming_show[0],
  }
  for i in past_show[1]:
    venue = Venue.query.filter_by(id=i.venue_id).first()
    data['past_shows'].append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(i.start_time)
    })
  for i in upcoming_show[1]:
    venue = Venue.query.filter_by(id=i.venue_id).first()
    data['upcoming_shows'].append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(i.start_time)
    })
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.filter_by(id=artist_id).first()
  #if form.validate_on_submit():
  form.name.data = artist.name
  form.genres.data = artist.genres
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.website_link.data = artist.website_link
  form.facebook_link.data = artist.facebook_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  form.image_link.data = artist.image_link
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  form = ArtistForm(request.form)
  if form.validate_on_submit():
    try:
      artist = Artist.query.get(artist_id)
      artist.name = form.name.data
      artist.genres = form.genres.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.website_link = form.website_link.data
      artist.facebook_link = form.facebook_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data
      artist.image_link = form.image_link.data
      db.session.commit()
    except:
      db.session.rollback()
      flash("Account could not be updated")
    #edit_error_handler()
  # artist record with ID <artist_id> using the new attributes
  else:
    if not facebook(request.form['facebook_link']):
      flash("Ensure your link is of the form https://www.facebook.com/")
    else:
      flash('Invalid_form. Please try again')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  form.name.data = venue.name
  form.genres.data = venue.genres
  form.address.data = venue.address
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.website_link.data = venue.website_link
  form.facebook_link.data = venue.facebook_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  form.image_link.data = venue.image_link
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  form = VenueForm(request.form)
  print(form.genres.data)
  if form.validate_on_submit():
    try:
      print('here1')
      venue = Venue.query.get(venue_id)
      venue.name = form.name.data
      venue.genres = form.genres.data
      venue.address = form.address.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.phone = form.phone.data
      venue.website_link = form.website_link.data
      venue.facebook_link = form.facebook_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data
      venue.image_link = form.image_link.data
      #edit_error_handler()
      db.session.commit()
      print('Here')
    except:
      db.session.rollback()
  # venue record with ID <venue_id> using the new attributes
  else:
    if not facebook(request.form['facebook_link']):
      flash("Ensure your link is of the form https://www.facebook.com/")
    else:
      flash('Invalid_form. Please try again')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  form = ArtistForm(request.form)
  print(form.genres.data)
  if form.validate_on_submit():
    try:
      # TODO: insert form data as a new Venue record in the db, instead
      #Gets each item from form and adds it to data with its data type in the database
      # TODO: modify data to be the data object returned from db insertion
      #insert data into db
      artist = Artist(
        name=form.name.data, 
        city=form.city.data, 
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website_link=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data 
      )
      #try_except(artist, "Artist ", form.name.data, form.name.data)
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + form.name.data + ' was successfully listed!')
      # on successful db insert, flash success
      #flash('Venue ' + form'name'] + ' was successfully listed!')
    except Exception as e:
      db.session.rollback()
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    # TODO: modify data to be the data object returned from db insertion
  else:
    if not facebook(request.form['facebook_link']):
      flash("Ensure your link is of the form https://www.facebook.com/")
    else:
      flash('Invalid_form. Please try again')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  show = Show.query.all()
  data = []
  for i in show:
    artist = Artist.query.get(i.artist_id)
    data.append({
      "venue_id": i.venue_id,
      "venue_name": (Venue.query.get(i.venue_id)).name,
      "artist_id": i.artist_id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(i.start_time)
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  if form.validate_on_submit():
    try:
      value = Show(artist_id=form.artist_id.data, venue_id=form.venue_id.data, start_time=form.start_time.data)
      check = Show.query.filter_by(start_time=form.start_time.data).all()
      """for i in check:
        if (i.venue_id == form.venue_id.data) and (i.artist_id == form.artist_id.data) and (i.start_time == form.start_time.data):
          flash("Show already exists.")
          return render_template('pages/home.html')"""
      # on successful db insert, flash success
      #try_except(value, "Show ")
      db.session.add(value)
      db.session.commit()
      #flash('Show was successfully listed!')
      return render_template('pages/home.html')
      # TODO: on unsuccessful db insert, flash an error instead.
    except:
      db.session.rollback()
      # e.g., flash('An error occurred. Show could not be listed.')
      flash("Invalid form. Get id from artist and venue page. Use the given date and time format")
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  else:
    flash("Invalid form. Get id from artist and venue page. Use the given date and time format")
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


"""# I declared thid function so as not to keep repeating myself
def try_except(value, table, success_name = '', fail_name = ''):
  try:
    db.session.add(value)
    db.session.commit()
    flash(table + success_name + ' was successfully listed!')
  except Exception as e:
    address = ''
    if table == 'Venue ':
      address = 'address'
    print(sys.exc_info())
    db.session.rollback()
    if "varying(120)" in str(sys.exc_info()):
      #flash('An error occurred. ' + table + fail_name + f''' could not be listed. 
      #  <p>Ensure your city, state, ' + {address} +', phone and facebook_link fields are no longer than 120 characters</p>''')
      flash(f'An error occurred. {table} {fail_name} could not be listed.\
        Hint:Ensure your city, state, {address}, phone and facebook_link fields are no longer than 120 characters')
    elif "varying(500)" in str(sys.exc_info()):
      flash('An error occurred. ' + table + fail_name + ' could not be listed.\
         Hint:Please ensure your image link is no longer than 500 characters')
    elif table == 'Show ':
      flash('An error occurred. ' + table + fail_name + ' could not be listed.\
         Hint:Get your artist id from the artist\'s page and the venue id from the venue\'s page.\
           Also ensure your time is in the format specified in the form.')
    else:
      flash('An error occurred. ' + table + fail_name + ' could not be listed. Your form is invalid')
    print(e)
  finally:
    db.session.close()"""


def upcoming(info, table):
  """
  Returns the number of upcoming shows and all upcoming shows in the database
  """
  if table == 'Venue':
    #shows = Show.query.filter_by(venue_id=info.id).all()
    shows = db.session.query(Show).join(Venue).filter(Show.venue_id==info.id).filter(Show.start_time>datetime.now()).all()
  else:
    #shows = Show.query.filter_by(artist_id=info.id).all()
    shows = db.session.query(Show).join(Artist).filter(Show.artist_id==info.id).filter(Show.start_time>datetime.now()).all()
  return len(shows), shows


def past(info, table):
  """
  Returns the number of upcoming shows and all upcoming shows in the database
  """
  if table == 'Venue':
    #shows = Show.query.filter_by(venue_id=info.id).all()
    shows = db.session.query(Show).join(Venue).filter(Show.venue_id==info.id).filter(Show.start_time<datetime.now()).all()
  else:
    #shows = Show.query.filter_by(artist_id=info.id).all()
    shows = db.session.query(Show).join(Artist).filter(Show.artist_id==info.id).filter(Show.start_time<datetime.now()).all()
  return len(shows), shows


"""def edit_error_handler():
  '''Error handler for editing routes e.g routes ending with /edit'''
  try:
    db.session.commit()
    flash("Data has been edited successfully")
  except:
    db.session.rollback()
    flash("Your data could not be edited. Please try again")
  finally:
    db.session.close()
  return None"""

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
