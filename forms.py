from datetime import datetime
from email.policy import default
from xml.dom import ValidationErr
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError
from enums import Genres, State
import re
from flask import flash
import dateutil

#Gotten from udacity code reviewer
def is_valid_phone(number):
    """ Validate phone numbers like:
    1234567890 - no space
    123.456.7890 - dot separator
    123-456-7890 - dash separator
    123 456 7890 - space separator

    Patterns:
    000 = [0-9]{3}
    0000 = [0-9]{4}
    -.  = ?[-. ]

    Note: (? = optional) - Learn more: https://regex101.com/
    """
    regex = re.compile('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
    if number == "":
        return True
    return regex.match(number)

def facebook(text):
    """Checks if the llink is a valid facebook link"""
    regex = re.compile('^(http|https)://(m.)?(www.)?facebook.com/')
    if text == '':
        return True
    return regex.match(text)

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

    def validate(self):
        try:
            self.artist_id.data = int(self.artist_id.data)
            self.venue_id.data = int(self.venue_id.data)
            self.start_time.data = dateutil.parser.parse(str(self.start_time.data))
        except:
            return False
        return True

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices= State.choices() # Had to remove the default since udacity code reviewer said i can follow DRY principle even on existing code
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices = Genres.choices() # Had to remove the default since udacity code reviewer said i can follow DRY principle even on existing code
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link'
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )

    #Udacity reviewer's code
    def validate(self):
        """Define a custom validate method in your Form:"""
        self.genres.data = [list_.split(",") for list_ in self.genres.data][0]
        if not is_valid_phone(self.phone.data):
            return False
        for i in self.genres.data:
            if not i in list(dict(Genres.choices()).values()):
                return False
        if self.state.data not in dict(State.choices()).keys():
            return False
        if not facebook(self.facebook_link.data):
            return False
        # if pass validation
        return True



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices = State.choices() # Had to remove the default since udacity code reviewer said i can follow DRY principle even on existing code
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices = Genres.choices() # Had to remove the default since udacity code reviewer said i can follow DRY principle even on existing code
     )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
     )

    website_link = StringField(
        'website_link'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )


    #Udacity reviewer's code
    def validate(self):
        """Define a custom validate method in your Form:"""
        self.genres.data = [list_.split(",") for list_ in self.genres.data][0]
        if not is_valid_phone(self.phone.data):
            return False
        for i in self.genres.data:
            if not i in list(dict(Genres.choices()).values()):
                return False
        if self.state.data not in dict(State.choices()).keys():
            return False
        if not facebook(self.facebook_link.data):
            return False
        # if pass validation
        return True