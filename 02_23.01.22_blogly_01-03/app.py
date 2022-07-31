"""Blogly application."""

from flask import Flask, render_template, redirect, url_for, flash, request;
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connectDB, Users;
from forms import UserForm;

app = Flask(__name__);

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['SQLALCHEMY_ECHO'] = True;
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['SECRET_KEY'] = 'wtf';

app.debug = True;
toolbar = DebugToolbarExtension(app);

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;

connectDB(app);    # 
db.create_all();    # create all relations/models associated with the db Instance, https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.SQLAlchemy.create_all

@app.route('/')
def indexView():
    '''Return a list of users.'''
    return '<body>hi</body>';   # fixed in a later exercise
    return '';

@app.route('/users/')
def usersView():
    '''Show a list of users, hyperlinked.'''
    #query and then save to a variable
    usersInformation = Users.returnUserList_alpha();
    return render_template('users.html',
        usersInformation = usersInformation);

@app.route('/users/new', methods=['GET', 'POST'])
def getNewUser():
    '''Form for creating a new user.'''

    form = UserForm();

    if form.validate_on_submit():
        
        formInformation = {
            "firstName": form.firstName.data,
            "lastName": form.lastName.data,
            "imageURL": form.imageLink.data
        };

        newUserInstance = Users(first_name=formInformation["firstName"], 
            last_name=formInformation["lastName"], 
            image_url=formInformation["imageURL"]);

        db.session.add(newUserInstance)
        db.session.commit();

        flash(f'New user, {formInformation["firstName"]} {formInformation["lastName"]}, Created!', 'success');
        return redirect(url_for('usersView'));
    
    else:
        return render_template('forms.html', form=form, formCancelOption=False)

@app.route('/users/<int:userID>', methods=['GET', 'POST'])  # 'POST' allowed to shortcut from a form because it is a 'POST' request
def viewUser(userID):
    '''View a user by ID.'''

    if request.method == "POST":
        # destroy any information by malicious actors attempting to take advantage of this 'POST' route even though it does nothing
        request.data = None;

    selectedUser = Users.returnUserByID(userID);

    if not selectedUser:     # maybe refactor into own method?
        return '404';

    return render_template('user.html',
        userInformation = selectedUser);

@app.route('/users/<int:userID>/edit', methods=['GET', 'POST'])
def editUser(userID):
    '''Edit a user by ID.'''
    selectedUser = Users.returnUserByID(userID);

    if not selectedUser:     # maybe refactor into own method?
        return '404';

    # do a pre-render of the form
    form = UserForm(
        firstName=selectedUser.first_name, 
        lastName=selectedUser.last_name, 
        imageLink=selectedUser.image_url)

    if form.validate_on_submit():
        selectedUser.first_name = form.firstName.data;
        selectedUser.last_name = form.lastName.data;
        selectedUser.image_url = form.imageLink.data;
        db.session.commit();
        flash('Information updated.', 'success');
        return redirect(f'/users/{userID}');

    else:
        return render_template('forms.html', form=form, formCancelOption=True, userID=userID);

@app.route('/users/<int:userID>/delete')
def deleteUserView(userID):
    '''Delete a user by ID.'''
    selectedUser = Users.returnUserByID(userID);

    if not selectedUser:     # maybe refactor into own method?
        return '404';
    
    db.session.delete(selectedUser);
    db.session.commit();
    flash('User deleted.', 'success');
    return redirect(url_for('usersView'));