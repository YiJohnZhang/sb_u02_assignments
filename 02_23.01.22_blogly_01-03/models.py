"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy;

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
"""
    @classmethod
    def createUser(cls):
        '''Creates a user.'''
    
    @classmethod
    def updateUser(cls):
        '''Updates a user information.'''

"""