"""Models for Blogly."""
from unittest import case
from flask_sqlalchemy import SQLAlchemy;
from datetime import datetime;              # timestamp for datetime.utcnow

db = SQLAlchemy();

def connectDB(app):
    db.app = app;
    db.init_app(app);   # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.SQLAlchemy.init_app

class Users(db.Model):

    '''ORM Representation of the User Relation.'''
    
    __tablename__ = "users";
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True);
    first_name = db.Column(db.String(35), nullable = False);
    last_name = db.Column(db.String(35), nullable = False);
    image_url = db.Column(db.Text, nullable = True);

    # https://realpython.com/python-property/#providing-read-only-attributes
    @property   # decorator method
    def fullName(self):
        '''Returns full name.'''
        return f'{self.first_name} {self.last_name}';

    def __repr__(self):
        '''Self-representation for instances of User ORM: '''
        instance = self;
        return f'<User Model: {instance.id}, {instance.first_name} {instance.last_name}>';

    def getFullName(self):
        '''Deprecated with @property fullName. Return the full name, rather than each property independently for maintainability.'''
        return f'{self.first_name} {self.last_name}';
    
    def getFullName_lastFirst(self):
        '''getFullName(self) but lastname, firstname'''
        return f'{self.last_name}, {self.first_name}';
    
    @classmethod
    def getUserList(cls):
        '''Returns a user list ordered by id.'''
        return cls.query.all();

    @classmethod
    def returnUserList_alpha(cls):
        '''Returns a user list ordered by alphabetical surname.'''
        return cls.query.order_by(Users.last_name).all();
    
    @classmethod
    def returnUserByID(cls, userID):
        '''Returns a user by id.'''
        return cls.query.get_or_404(userID);

class Posts(db.Model):
    '''ORM Representation of a Post Relation.'''

    id = db.Column(db.Integer, auto_increment = True, primary_key = True);
    title = db.Column(db.String(50), nullable = False);
    content = db.Column(db.Text, nullable = False);
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'));
    author = db.relationship('Users', backref=db.backref("posts", passive_deletes=True));

    @property
    def displayedPostTitle(self):
        
        displayTitle = self.title;
        
        if len(displayTitle) >= 15:
            displayTitle = self.title[0:12]+"...";

        return displayTitle;

    def __repr__(self):
        return f'<Posts Model: Post {self.id} by {self.author_id}>'

    def updatePost(self, title, content):
        self.title = title;
        self.content = content;
        db.session.add(self);
        db.session.commit();

    @classmethod
    def returnPostsByUserID(cls, userID):
        return cls.query.filter(cls.author_id==userID).all();
    
    @classmethod
    def returnPostByID(cls, postID):
        return cls.query.get_or_404(postID);
    