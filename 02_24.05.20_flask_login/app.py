from flask import Flask, session, render_template, redirect, url_for, request, abort, flash;
from models import db, connectDB, User, Feedback;
from forms import LoginForm, RegisterForm, FeedbackForm;
from secrets import API_SECRET_KEY;
from flask_debugtoolbar import DebugToolbarExtension;

app = Flask(__name__);

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sb_24.05.20'; 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['SQLALCHEMY_ECHO'] = False;
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1;

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

def checkCredentials(username):
    return username == session['username'];

# def redirectAuthenticatedPublicViews():
#     # apparently view focus is lost
#     return redirect(url_for('userView', username=session['username']));

# def preventAuthenticatedPublicViews():
#     if checkSession():
#         redirectAuthenticatedPublicViews();

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

    if checkSession():      # note: need to figure out how to handle all this logic with one callback
        return redirect(url_for('userView', username=session['username']));

    registerForm = RegisterForm();

    if registerForm.validate_on_submit():

        userObject = User.createUser(request.form);

        if userObject:
            session['username'] = userObject.username;
            return redirect(url_for('userView', username=session['username']));
        
        flash('Username already taken.', category='error')

    return render_template('forms.html',
        form=registerForm, formPurpose='register');

@app.route('/login', methods=['GET', 'POST'])
def loginView():

    if checkSession():      # note: need to figure out how to handle all this logic with one callback
        return redirect(url_for('userView', username=session['username']));
    
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

    else:   # because flask insists there is an "IndentationError: unexpected indent"
        flash('You must be logged in to do that!', category='error');
        return redirect(url_for('indexView'));

@app.route('/users/<username>')
def userView(username):

    if not checkSession():      # note: need to figure out how to handle all this logic with one callback
        flash('You must be logged in to do that!', category='error');
        return redirect(url_for('indexView'));
    
    if not checkCredentials(username):  # need to figure out how to handle all this lgoic with one callback, too
        abort(401);

    feedbackList = Feedback.listFeedbackByUserID(username);

    return render_template('user.html', feedbackList=feedbackList);

@app.route('/users/<username>/delete', methods=['POST'])
def deleteUserView(username):

    if not checkSession():      # note: need to figure out how to handle all this logic with one callback
        flash('You must be logged in to do that!', category='error');
        return redirect(url_for('indexView'));
       
    if not checkCredentials(username):  # need to figure out how to handle all this lgoic with one callback, too
        abort(401);

    session.pop('username');    # logout
    flash(f'{username} has been successfully deleted!');
        
    return redirect(url_for('indexView'));


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def addFeedbackView(username):
    
    if not checkSession():      # note: need to figure out how to handle all this logic with one callback
        flash('You must be logged in to do that!', category='error');
        return redirect(url_for('indexView'));
       
    if not checkCredentials(username):  # need to figure out how to handle all this lgoic with one callback, too
        abort(401);
    
    feedbackForm = FeedbackForm();

    if feedbackForm.validate_on_submit():

        Feedback.createFeedback(request.form, session['username']);
        flash('Thank you for your feedback!', category='success');
        
        return redirect(url_for('userView', username=username));

    
    return render_template('forms.html',
        form=feedbackForm, formPurpose='feedback', username=username);

@app.route('/feedback/<int:feedbackID>/update', methods=['GET', 'POST'])
def updateFeedbackView(feedbackID):

    if not checkSession():      # note: need to figure out how to handle all this logic with one callback
        flash('You must be logged in to do that!', category='error');
        return redirect(url_for('indexView'));

    selectedFeedback = Feedback.searchFeedbackByID(feedbackID);

    if not selectedFeedback:
        abort(404);

    expectedUsername = selectedFeedback.author;

    if not checkCredentials(expectedUsername):  # need to figure out how to handle all this lgoic with one callback, too
        abort(401);

    #inject feedback data selectedFeedback
    feedbackForm = FeedbackForm(obj=selectedFeedback);

    if feedbackForm.validate_on_submit():
        selectedFeedback.updateFeedback(request.form);
        flash(f'Updated {selectedFeedback} successfully!', category='success');
        return redirect(url_for('userView', username=selectedFeedback.author));

    return render_template('forms.html', form = feedbackForm);

@app.route('/feedback/<int:feedbackID>/delete', methods=['POST'])
def deleteFeedbackView(feedbackID):

    if not checkSession():      # note: need to figure out how to handle all this logic with one callback
        flash('You must be logged in to do that!', category='error');
        return redirect(url_for('indexView'));
       
    selectedFeedback = Feedback.searchFeedbackByID(feedbackID);

    if not selectedFeedback:
        abort(404);

    if not checkCredentials(selectedFeedback.author):  # need to figure out how to handle all this lgoic with one callback, too
        abort(401);
    
    expectedUsername = selectedFeedback.author;

    if not checkCredentials(expectedUsername):  # need to figure out how to handle all this lgoic with one callback, too
        abort(401);

    selectedFeedback.deleteFeedback();
    flash(f'Deleted {selectedFeedback} successfully!', category='success');

    return redirect(url_for('userView', username=selectedFeedback.author));