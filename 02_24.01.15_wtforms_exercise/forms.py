from flask_wtf import FlaskForm;
from wtforms.fields import StringField, TextAreaField, IntegerField, BooleanField, HiddenField;
from wtforms.validators import InputRequired, Optional, NumberRange, URL, Length;

class PetAddEditForm(FlaskForm):
    # attach a class and do a hackey way of rendering in the Jinja template because
    photo_url = StringField("Photo URL (Optional): ",
        validators=[Optional(), URL(require_tld=False, message="Enter a valid URL.")],
        description="renderLater");
    notes = TextAreaField("Description: ",
        validators=[Optional(), Length(max=4096, message="Please keep the description < 4096 characters.")],
        render_kw={
            'class':'block textarea'
        },
        description="renderLater");

class PetAddForm(PetAddEditForm):
    # attach a class and do a hackey way of rendering in the Jinja template because
    name = StringField("Pet Name: ",
        validators=[InputRequired()]);
    species = StringField("Species:",
        validators=[InputRequired()]);
    age = IntegerField("Age: ",
        validators=[Optional(), NumberRange(min=0, max=30, message="Please enter a valid age.")]);

class PetEditForm(PetAddEditForm):
    available = BooleanField("Is Available?",
        render_kw={
        #    'checked':True
        },
        false_values=[False],     # so that it will return rather than be a null value
        description="renderLater");
    # php hack for this: https://stackoverflow.com/questions/1809494/post-unchecked-html-checkboxes
    # hackAvailable = HiddenField("Hackey override",
    #     name = 'available',
    #     render_kw={
    #         'value':0
    #     });

# class BasePetForm(FlaskForm):
#     def __iter__(self):
#         # inspiration: https://stackoverflow.com/questions/5848252/wtforms-form-class-subclassing-and-field-ordering
#         fieldOrder = getattr(self, 'fieldOrder', None);     # so self, as in this instance; find a `fieldOrder` attr, set as None o.w.
#         if fieldOrder:
            

# class PetAddForm(FlaskForm):
#     '''Things exlcusive to "Add Pet" form.'''
    

# class PetAddEditForm(FlaskForm):
#     '''Everything in common with the "Add Pet" and "Edit Pet" forms.'''


# class PetEditForm(FlaskForm):
#     '''Form Field exclusive to "Edit Pet" form.'''
