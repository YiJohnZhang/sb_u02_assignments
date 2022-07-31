from flask_wtf import FlaskForm;
from wtforms import StringField, TextAreaField;
from wtforms.validators import InputRequired, Optional;

class UserForm(FlaskForm):
    '''Form to add/edit Users.'''
    firstName = StringField("First Name",
        validators=[InputRequired()]);
    lastName = StringField("Last Name",
        validators=[InputRequired()]);
    imageLink = StringField("Image URL",
        validators=[Optional()]);

class PostForm(FlaskForm):
    '''Form to add/edit Posts.'''
    postTitle = StringField("Title",
        validators=[InputRequired()]);
    postContent = TextAreaField("Content",
        render_kw={"rows":5, "cols":50});