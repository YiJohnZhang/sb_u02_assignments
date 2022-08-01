from flask_wtf import FlaskForm;
from wtforms import StringField, SelectField, DecimalField, URLField;
from wtforms.validators import InputRequired, Optional, Length, NumberRange, URL;

class CupcakeForm(FlaskForm):
    
    flavor = StringField('Flavor: ', validators=[InputRequired('Input Required'), Length(max=16, message='Input between the first 16 characters of the flavor.')]);
    size = SelectField('Size: ', validators=[InputRequired()], coerce=int, validate_choice=True);
    rating = DecimalField('Rating: ', validators=[InputRequired(), NumberRange(min = 0.0, max = 10, message='Input a number between 0.0 and 10.0.')]);
        # [`DecimalField` is preferred to `FlaotField``](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.FloatField)
    image = URLField('Image URL: ', validators=[Optional(), URL(message='Enter a valid URL.')], filters = [lambda x: x or None]);
        # I can't default an empty string to None ._.