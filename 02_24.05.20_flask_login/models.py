# from app import bcrypt;   # circular import b/c app.py imports models.py
from flask_sqlalchemy import SQLAlchemy;
from flask_bcrypt import Bcrypt;

db = SQLAlchemy();
bcrypt = Bcrypt();

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
    is_admin = db.Column(db.Boolean, nullable=True, default=False);     # extra protection for nullable=True to create None types.

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

        if not cls.searchUserByUsername(data['username']):

            userObject = cls(**data);
            userObject.password= cls.hashString(data['password'])
            print(userObject)

            db.session.add(userObject);
            db.session.commit();

            return userObject;

        else:
            return None;    # error that the user already exists
        
    @classmethod
    def searchUserByUsername(cls, username):
        '''Search the database by username.'''
        print(username);
        return cls.query.filter(cls.username==username).first();
    
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

    # Admin Methods
    @property
    def admin_UserVerbose(self):
        '''User object representation visible to admins.'''
        return f'User {self.username}: {self.last_name}, {self.first_name}';

    @classmethod
    def admin_returnAllUsersButAdmins(cls):
        '''Admin Feedback Search.'''
        return cls.query.filter(User.is_admin != True).all();  # prevents admins from banning admins 
    

    # @classmethod
    # def searchUserByUsername(cls, username):
    #     '''Admin User search'''
    #     return cls.query.get_or_404(username);

    @classmethod
    def admin_banAndDeleteUser(cls, username):
        '''Admin Feedback Delete.'''
        
        selectedUser = cls.searchUserByUsername(username);

        if selectedUser:
            try:
                db.session.delete(selectedUser);
                db.session.commit();
            except Exception as error:
                db.session.flush();
                db.session.rollback();
                return error;

        else:
            return f'<User {username}> does not exist!';

class Feedback(db.Model):

    __tablename__ = 'feedback';

    id = db.Column(db.Integer, autoincrement=True, primary_key=True);
    title = db.Column(db.String(100), nullable=False);
    content = db.Column(db.Text, nullable=False);

    author = db.Column(db.String(20), db.ForeignKey(User.username, ondelete='CASCADE', onupdate='CASCADE'));
    authorReference = db.relationship('User', backref=db.backref('feedbackReference', passive_deletes=True));

    def __repr__(self):
        '''Self-representation for a feedback object.'''
        if len(self.title) > 25:
            displayedTitle = f'{self.title[0:22]}...';
        else:
            displayedTitle = self.title;

        return f'<Feedback {self.id}: {displayedTitle}>';

    @classmethod    # could potentially create a prototype because the function is similar
    def cleanRequestData(cls, requestData):
        '''Cleans request data. Such as removing the `csrf_token` so that it doesn't mess with kwarg-ing a Model creation.'''

        mutableRequestData = dict(requestData);

        if mutableRequestData.get('csrf_token'):
            mutableRequestData.pop('csrf_token');
    
        return mutableRequestData;

    @classmethod
    def createFeedback(cls, requestData, author):
        '''Create a new Feedback object.'''

        data = Feedback.cleanRequestData(requestData);
        data['author'] = str(author);

        feedbackObject = cls(**data);
        User.query.get(feedbackObject.author);
        db.session.add(feedbackObject);     # error here, apparently User.query.get('asdf') == feedbackObject.username, where username passed is 'asdf' returns false
        db.session.commit();

        return;

    @classmethod
    def searchFeedbackByID(cls, feedbacKID):
        '''Searches Feedback by the ID (primary key).'''
        return cls.query.get_or_404(feedbacKID);

    @classmethod
    def listFeedbackByUserID(cls, author):
        '''Searches Feedback by the User ID (parent foreign key).'''
        return cls.query.filter(cls.author == author).all();

    @classmethod
    def authorizeFeedbackOperation(cls, feedbackID, author):
        '''Authorize a Feedback manipulation operation by checking if the attempting user is the original author.'''

        if cls.searchFeedbackByID(feedbackID).author == author:     # Reminder: pass username = userObject.username from sessions.
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

    # Admin Methods
    @property
    def admin_FeedbackVerbose(self):
        '''Feedback object representation visible to admins.'''
        return f'Feedback {self.id}: {self.title} by {self.author}\n{self.content}.';

    @classmethod
    def admin_returnAllFeedback(cls):
        '''Admin Feedback Search.'''
        return cls.query.all();

    @classmethod
    def admin_deleteFeedback(cls, feedbackID):
        '''Admin Feedback Delete.'''
        
        selectedFeedback = cls.searchFeedbackByID(feedbackID);

        if selectedFeedback:
            try:
                db.session.delete(selectedFeedback);
                db.session.commit();
            except Exception as error:
                db.session.flush();
                db.session.rollback();
                return error;

        else:
            return f'<Feedback {feedbackID}> does not exist!';
