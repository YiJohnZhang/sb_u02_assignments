"""Models for Blogly."""
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
    
    __tablename__ = "posts";

    id = db.Column(db.Integer, autoincrement = True, primary_key = True);
    title = db.Column(db.String(50), nullable = False);
    content = db.Column(db.Text, nullable = False);
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'));
    author = db.relationship('Users', backref=db.backref("posts", passive_deletes=True));

    # postTagJoin = db.relationship('Posts',
    #     backref='postJoin', cascade='all, delete');

    tagThrough = db.relationship('Tags',
        secondary='posts_tags_join',
        backref='postThrough');

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
    def returnAllPosts(cls):
        return cls.query.all();

    @classmethod
    def returnPostsByUserID(cls, userID):
        return cls.query.filter(cls.author_id==userID).all();
    
    @classmethod
    def returnPostByID(cls, postID):
        return cls.query.get_or_404(postID);

class Tags(db.Model):
    
    __tablename__ = "tags";

    id = db.Column(db.Integer, autoincrement=True, primary_key=True);
    tag_name = db.Column(db.String(10), nullable=False, unique=True);

    # postTagJoin = db.relationship('Tags',
    #     backref='tagJoin', cascade='all, delete');

    #class methods: return posts by tag, get tags from post, return all tags
    @classmethod
    def returnTagList(cls):
        return cls.query.all();
    
    @classmethod
    def returnTagByID(cls, tagID):
        return cls.query.get_or_404(tagID);

    @classmethod
    def createTag(cls, data):
        db.session.add(Tags(**data));
        db.session.commit();
        return;
    
    @classmethod
    def updateTag(cls, tagInstance, data):
        cls.query.filter(cls.id == tagInstance.id).update(data);
        db.session.commit();
        return;
    
    @classmethod
    def cleanRequestFormData(cls, requestData):
        mutableRequestData = dict(requestData);

        if mutableRequestData['csrf_token']:
            mutableRequestData.pop('csrf_token');
        
        if mutableRequestData['linked_posts']:
        #    print(mutableRequestData['linked_posts'])
            mutableRequestData.pop('linked_posts');
        
        return mutableRequestData;

    def deleteTag(self):
        db.session.delete(self);
            # potentially need to query by self.id
        db.session.commit();
        return;

    def returnInstanceAttributes(self):
        return vars(self);
        

class PostsTagsJoin(db.Model):

    __tablename__ = 'posts_tags_join';

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'), primary_key = True);
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'), primary_key = True);
        
    postJoin = db.relationship('Posts',
        backref=db.backref('postTagJoin', cascade='all, delete'));

    tagJoin = db.relationship('Tags',
        backref=db.backref('postTagJoin', cascade='all, delete'));

    def __repr__(self):
        return f'<PostsTagsJoin: Post {self.post_id}, Tag {self.tag_id}>';

    @classmethod
    def returnEntriesContainingPostByID(cls, postID):
        return cls.query.filter(cls.post_id == postID).all();

    @classmethod
    def returnEntriesContainingTagByID(cls, tagID):
        return cls.query.filter(cls.tag_id == tagID).all();

    