# from app import bcrypt;   # circular import b/c app.py imports models.py
from flask_sqlalchemy import SQLAlchemy;

db = SQLAlchemy();

def connectDB(app):
    db.app = app;
    db.init_app(app);

class User(db.Model):

    __tablename__ = 'users';

    username = db.Column(db.String(20), unique=True, primary_key=True);
    password = db.Column(db.Text, nullable=False);
    email = db.Column(db.String(50), unique=True, nullable=False);
    first_name = db.Column(db.String(30), nullable=False);
    last_name = db.Column(db.String(30), nullable=False);

    def __repr__(self):
        '''Self-representation for a user object.'''
        return f'<User {self.username}: {self.first_name}>';
    
    @classmethod
    def cleanRequestData(cls, requestData):
        '''Cleans request data. Such as removing the `csrf_token` so that it doesn't mess with kwarg-ing a Model creation.'''
        mutableRequestData = dict(requestData);

        if mutableRequestData.get('csrf_token'):
            mutableRequestData.pop('csrf_token');
    
        return mutableRequestData;
    
    @classmethod
    def hashString(cls, stringToHash):
        '''Return utf-8 decoded hash of a passed string to hash, such as a password.'''
        
        hashedString = bcrypt.generate_password_hash(stringToHash);
        utf8_hashedString = hashedString.decode('utf-8');

        return utf8_hashedString;
    
    @classmethod
    def authorizeUserOperation(cls, userPath, username):
        
        if cls.searchUserByUsername(userPath) == username:     # Reminder: pass username = userObject.username from sessions; userPath = the view variable routing
            return True;
        else:
            return False;    # use to trigger an error

    @classmethod
    def createUser(cls, requestData):
        '''Create a new user object; register a user.'''

        data = cls.cleanRequestData(requestData);

        if not cls.searchUserByUsername(requestData.get('username')):
            
            print('------------')
            
            userObject = cls(**data);
            userObject['password']= cls.hashString(data['password'])
            print(userObject)

            db.session.add(userObject);
            db.session.commit();

            return userObject;

        else:
            return None;    # error that the user already exists
        
    @classmethod
    def searchUserByUsername(cls, username):
        '''Search the database by username.'''
        return cls.query.filter(cls.username==username).first_or_404();
    
    @classmethod
    def authenticateUserLogin(cls, username, password):
        '''Authetnicate the entered credentials.'''

        userObject = cls.searchUserByUsername(username);

        if userObject and bcrypt.check_password_hash(userObject.password, password):
            return userObject;
        else:
            return False;   # not found or password/user combination incorrect

    def deleteUser(self, userPath, username):
        
        if User.authorizeUserOperation(userPath, username):     # Reminder: pass username = userObject.username from sessions.
            db.session.delete(self);
            db.session.commit();
            return;
        else:
            return False;    # use to trigger an error

class Feedback(db.Model):

    __tablename__ = 'feedback';

    id = db.Column(db.Integer, autoincrement=True, primary_key=True);
    title = db.Column(db.String(100), nullable=False);
    content = db.Column(db.Text, nullable=False);

    username = db.Column(db.ForeignKey(User.username, ondelete='CASCADE', onupdate='CASCADE'));
    userReference = db.relationship('User', backref=db.backref('feedbackReference', passive_deletes=True));

    @classmethod    # could potentially create a prototype because the function is similar
    def cleanRequestData(cls, requestData):
        '''Cleans request data. Such as removing the `csrf_token` so that it doesn't mess with kwarg-ing a Model creation.'''

        mutableRequestData = dict(requestData);

        if mutableRequestData.get('csrf_token'):
            mutableRequestData.pop('csrf_token');
    
        return mutableRequestData;

    @classmethod
    def createFeedback(cls, requestData):
        '''Create a new Feedback object.'''
        return;

    @classmethod
    def searchFeedbackByID(cls, feedbacKID):
        '''Searches Feedback by the ID (primary key).'''
        return cls.query.get_or_404(feedbacKID);

    @classmethod
    def authorizeFeedbackOperation(cls, feedbackID, username):
        '''Authorize a Feedback manipulation operation by checking if the attempting user is the original author.'''

        if cls.searchFeedbackByID(feedbackID).username == username:     # Reminder: pass username = userObject.username from sessions.
            return True;
        else:
            return False;


    def updateFeedback(self, requestData):
        '''Update the Feedback object.'''

        data = Feedback.cleanRequestData(requestData);

        db.session.query(Feedback).filter(Feedback.id == self.id).update(data);
        db.session.commit();
        return;

    def deleteFeedback(self):
        '''Delete the Feedback entry.'''
        db.session.delete(self);
        db.session.commit();
        return;



