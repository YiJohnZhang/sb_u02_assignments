from flask_wtf import FlaskForm;
from wtforms import widgets, StringField, TextAreaField, SelectMultipleField, SelectField;
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
    linked_tags = SelectMultipleField('Edit Tag(s) with the Post:', coerce=int,
        render_kw={
            'class':'block'
        });

# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()

class TagForm(FlaskForm):

    # Method 02: Custom Constructor
    # def __init__(self, multiFieldInformation, *args, **kwargs):
    #     super(TagForm, self).__init__(*args, **kwargs);
    #     self.multiFieldInformation = multiFieldInformation;
    #     self.test = MultiCheckboxField('Edit Posts withs the Tag:', choices=self.multiFieldInformation)

    '''Form to add/edit Tags.'''
    tag_name = StringField("Tag Name",
        render_kw={
            'maxlength':10
        },
        validators=[InputRequired()]);

    linked_posts = SelectMultipleField('Edit Post(s) with the Tag:', coerce=int,
        render_kw={
            'class':'block'
        });

    # Method 01: Vanilla .choices Injection; Form Modification w/ hard-coded side-by-side
    # test = SelectMultipleField('testFieldtagFormInstance', coerce=int);
    # test = SelectMultipleField('test', choices=[('ads','asdf'),('asdff','ffffa')]);

    # edit_posts_with_tags = MultiCheckboxField('Edit Posts with the Tag:',
    #     choices=[('one','one'), ('two', 'two')]);
        # Source: https://wtforms.readthedocs.io/en/3.0.x/specific_problems/?highlight=multicheckboxfield#specialty-field-tricks
        # Source: https://stackoverflow.com/questions/45178766/how-to-stack-vertically-or-horizontally-two-multicheckboxfield-wtform-fields
        # https://gist.github.com/juzten/2c7850462210bfa540e3