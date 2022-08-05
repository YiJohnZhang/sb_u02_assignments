from flask import Flask, session, render_template, redirect, url_for, request, abort, flash;
from models import db, connectDB, User, Feedback;
from forms import LoginForm, RegisterForm, FeedbackForm;
from flask_bcrypt import Bcrypt;
from secrets import API_SECRET_KEY;
from flask_debugtoolbar import DebugToolbarExtension;

app = Flask(__name__);
bcrypt = Bcrypt();

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sb_24.05.20'; 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['SQLALCHEMY_ECHO'] = False;
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
# Sessions
app.config['SECRET_KEY'] = API_SECRET_KEY;
# DebugToolbar
app.debug = True;
toolbar = DebugToolbarExtension(app);
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;

connectDB(app);
db.create_all();


# Handle Public View Routing
def checkSession():
    return 'username' in session;

def redirectAuthenticatedPublicViews():
    return redirect(url_for('userView', username=session['username']));

def preventAuthenticatedPublicViews():
    if checkSession():
        redirectAuthenticatedPublicViews();

# Error Views
@app.errorhandler(401)
def unauthorizedView_401(error):
    return ('401: Unauthorized.', 401);

@app.errorhandler(404)
def notFoundView_404(error):
    return ('404: Not Found', 404);

# Public Views
@app.route('/')
def indexView():
    return render_template('base.html');

@app.route('/register', methods=['GET', 'POST'])
def registerView():

    preventAuthenticatedPublicViews();

    registerForm = RegisterForm();

    if registerForm.validate_on_submit():

        # stopes here
        userObject = User.createUser(request.form);

        if userObject:
            session['username'] = userObject.username;
            return redirect(url_for('userView', username=session['username']));
        
        flash('Username already taken.', category='error')

    return render_template('forms.html',
        form=registerForm, formPurpose='register');

@app.route('/login', methods=['GET', 'POST'])
def loginView():

    preventAuthenticatedPublicViews();
    
    loginForm = LoginForm();

    if loginForm.validate_on_submit():

        credentialsMatch = User.authenticateUserLogin(request.form['username'], request.form['password']);

        if credentialsMatch:
            session['username'] = credentialsMatch.username;
            return redirect(url_for('userView', username=session['username']));
        
        flash('Invalid username/password combination', category='error');

    return render_template('forms.html',
        form=loginForm, formPurpose='login');

# Authentication Required Views
@app.route('/logout')
def logoutView():

    if checkSession():
        session.pop('username');
        return redirect(url_for('indexView'));
    
    flash('You must be logged in to do that.')
    return abort(401);

@app.route('/users/<username>')
def userView(username):

    return 'asfd';

@app.route('/users/<username>/delete', methods=['POST'])
def deleteUserView(username):
    return;

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def addFeedbackView(username):
    
    feedbackForm = FeedbackForm();
    
    return render_template('forms.html',
        form=feedbackForm, formPurpose='feedback', username=username);

@app.route('/feedback/<int:feedbackID>/update', methods=['GET', 'POST'])
def updateFeedbackView(feedbackID):
    return;

@app.route('/feedback/<int:feedbackID>/delete', methods=['POST'])
def deleteFeedbackView(feedbacKID):

    username = session['username'];



    return redirect(url_for('userView', username=username));