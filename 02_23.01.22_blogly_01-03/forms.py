from flask_wtf import FlaskForm;
from wtforms import StringField;
from wtforms.validators import InputRequired, Optional;

class UserForm(FlaskForm):
    '''Form to add/edit Users.'''
    firstName = StringField("First Name",
        validators=[InputRequired()]);
    lastName = StringField("Last Name",
        validators=[InputRequired()]);
    imageLink = StringField("Image URL",
        validators=[Optional()]);