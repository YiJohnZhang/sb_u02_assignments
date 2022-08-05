from flask import Flask, session, render_template, redirect, url_for, abort, flash;
from models import db, connectDB, User, Feedback;
from forms import LoginForm, RegisterForm;
from secrets import API_SECRET_KEY;

app = Flask(__name__);

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'; 
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

# Error Views
@app.errorhandler(401)
def unauthorizedView_401():
    return '401: Unauthorized.';

@app.errorhandler(404)
def notFoundView_404():
    return '404: Not Found';

# Public Views
@app.route('/')
def indexView():
    return;

@app.route('/register', methods=['GET', 'POST'])
def registerView():

    return;

@app.route('/login', methods=['GET', 'POST'])
def loginView():
    
    return;

# Authentication Required Views
@app.route('/logout')
def logoutView():

    if 'username' in session:
        session.pop('username');
        return redirect(url_for('indexView'));
    
    flash('You must be logged in to do that.')
    return abort(401);

@app.route('/users/<username>')
def userView(username):

    return;

@app.route('/users/<username>/delete', methods=['POST'])
def deleteUserView(username):
    return;

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def addFeedbackView(username):
    return;

@app.route('/feedback/<int:feedbackID>/update', methods=['GET', 'POST'])
def updateFeedbackView(feedbackID):
    return;

@app.route('/feedback/<int:feedbackID>/delete', methods=['POST'])
def deleteFeedbackView(feedbacKID):

    username = session['username'];

    

    return redirect(url_for('userView', username=username));