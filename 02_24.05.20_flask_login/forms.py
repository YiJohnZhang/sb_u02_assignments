from flask_wtf import FlaskForm;
from wtforms import StringField, PasswordField, TextAreaField;
from wtforms.validators import InputRequired, Length;

class LoginForm(FlaskForm):
    
    username = StringField(label='Username', validators=[InputRequired(), Length(min=1, max=20)]);
    password = PasswordField(label='Password',validators=[InputRequired()]);

class RegisterForm(LoginForm):
    
    email = StringField(label='Email', validators=[InputRequired(), Length(min=1, max=50)]);
    first_name = StringField(label='First Name', validators=[InputRequired(), Length(max=30)]);
    last_name = StringField(label='Last Name', validators=[InputRequired(), Length(max=30)]);


class FeedbackForm(FlaskForm):

    title = StringField(label='Title', validators=[InputRequired()]);
    content = TextAreaField(label='Feedback Form', validators=[InputRequired()]);