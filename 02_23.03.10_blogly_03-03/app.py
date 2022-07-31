"""Blogly application."""

from flask import Flask, render_template, redirect, url_for, flash, request;
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connectDB, Users, Posts, Tags, PostsTagsJoin;
from forms import UserForm, PostForm, TagForm;

app = Flask(__name__);

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['SQLALCHEMY_ECHO'] = False;
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

@app.route('/users')
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
        return render_template('forms_users.html', form=form, formCancelOption=False);

@app.route('/users/<int:userID>', methods=['GET', 'POST'])  # 'POST' allowed to shortcut from a form because it is a 'POST' request
def viewUser(userID):
    '''View a user by ID.'''

    if request.method == "POST":
        # destroy any information by malicious actors attempting to take advantage of this 'POST' route even though it does nothing
        request.data = None;

    selectedUser = Users.returnUserByID(userID);

    if not selectedUser:     # maybe refactor into own method?
        return '404';

    foundPosts = Posts.returnPostsByUserID(userID);

    return render_template('user.html',
        userInformation = selectedUser,
        userPosts = foundPosts);

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
        return render_template('forms_users.html', form=form, formCancelOption=True, userID=userID);

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

# Posts
@app.route('/posts/<int:postID>')
def viewPostView(postID):
    
    selectedPost = Posts.returnPostByID(postID);
    if not selectedPost:        # maybe refactor and combine with "if not selectedUser:"
        return '404';
    
    selectedUser = Users.returnUserByID(selectedPost.author_id);

    associatedTags = PostsTagsJoin.returnEntriesContainingPostByID(postID);

    return render_template('post.html',
        tagInformation = associatedTags,
        postInformation=selectedPost, userInformation=selectedUser);

@app.route('/posts/<int:postID>/edit', methods=['GET', 'POST'])
def editPostView(postID):

    selectedPost = Posts.returnPostByID(postID);
    if not selectedPost:        # maybe refactor and combine with "if not selectedUser:"
        return '404';

    postFormInstance = PostForm(postTitle=selectedPost.title, postContent=selectedPost.content);

    postFormInstance.linked_tags.choices = [(tag.id, tag.tag_name) for tag in Tags.returnTagList()];


    if postFormInstance.validate_on_submit():
        selectedPost.updatePost(title=postFormInstance.postTitle.data, content=postFormInstance.postContent.data);
        return redirect(f'/posts/{postID}');
    else:
        return render_template('forms_posts.html',
            form=postFormInstance, postInformation=selectedPost, formType='editPost');

@app.route('/users/<int:userID>/posts/new', methods=['GET', 'POST'])
def newPostView(userID):

    selectedUser = Users.returnUserByID(userID);

    if not selectedUser:     # maybe refactor into own method?
        return '404';

    postFormInstance = PostForm();

    postFormInstance.linked_tags.choices = [(tag.id, tag.tag_name) for tag in Tags.returnTagList()];

    if postFormInstance.validate_on_submit():
        newPost = Posts(title=postFormInstance.postTitle.data, content=postFormInstance.postContent.data, author_id=userID);
        db.session.add(newPost);
        db.session.commit();
        return redirect(f'/users/{userID}');
    
    else:
        return render_template('forms_posts.html', 
            userInformation=selectedUser, 
            form=postFormInstance, formType='newPost');

@app.route('/posts/<int:postID>/delete')
def deletePostView(postID):
    
    selectedPost = Posts.returnPostByID(postID);
    if not selectedPost:        # maybe refactor and combine with "if not selectedUser:"
        return '404';
    
    db.session.delete(selectedPost)
    db.session.commit();

    return redirect(url_for('usersView'));

# Tags
@app.route('/tags')
def tagView():

    listOfTags = Tags.returnTagList();
    
    return render_template('tags.html', tagInformation = listOfTags);
    
    
@app.route('/tags/<int:tagID>')
def viewTagView(tagID):

    selectedTag = Tags.returnTagByID(tagID);
    if not selectedTag:
        return '404';

    selectedPostTagInformation = PostsTagsJoin.returnEntriesContainingTagByID(tagID);

    return render_template('tag.html',
        tagInformation = selectedTag,
        postTagInformation = selectedPostTagInformation);

@app.route('/tags/new', methods=['GET', 'POST'])
def createTagView():

    
    tagFormInstance = TagForm();
    tagFormInstance.linked_posts.choices = [(post.id, post.title) for post in Posts.returnAllPosts()];
        #and after 12 hours of anguish, meer-a-cull, sa mar-sch!

    # Method 01: Vanilla .choices Injection
    # foo = [('ads','asdf'),('asdff','ffffa')];
    # tagFormInstance.test.choices = [('ads','asdf'),('asdff','ffffa')];  # this is cursed. I can't inject .choices with this.
    # tagFormInstance.test.choices = foo;  # this is cursed. I can't inject .choices with this.

    # Method 02: Custom Constructor
    # foo = [('ads','asdf'),('asdff','ffffa')]
    # tagFormInstance = TagForm(multiFieldInformation = foo);
    
    # selectMultipleField
    # for some reason teh below choices is not reach the tagFormInstance....
    # tagFormInstance.edit_posts_with_tags.choices = [(1, 'hello'), (2, 'goodbye'), (3, 'here')];
    #tagFormInstance.test.choices = [(1, 'hello'), (2, 'goodbye'), (3, 'here')];
        #[(post.id, post.title) for post in Posts.returnAllPosts()];

    if tagFormInstance.validate_on_submit():

        requestFormData = Tags.cleanRequestFormData(request.form);
        Tags.createTag(requestFormData);

        return redirect(url_for('tagView'));

    else:

        return render_template('forms_tags.html',
            form=tagFormInstance,
            formType='newTag');
 
@app.route('/tags/<int:tagID>/edit', methods=['GET', 'POST'])
def updateTagView(tagID):

    selectedTag = Tags.returnTagByID(tagID);
    if not selectedTag:
        return '404';

    tagFormInstance = TagForm(**(selectedTag.returnInstanceAttributes()));
    tagFormInstance.linked_posts.choices = [(post.id, post.title) for post in Posts.returnAllPosts()];

    if tagFormInstance.validate_on_submit():
        
        requestFormData = Tags.cleanRequestFormData(request.form);
        print(requestFormData);
        Tags.updateTag(selectedTag, requestFormData);

        return redirect(f'/tags/{tagID}');

    else:

        return render_template('forms_tags.html',
            form=tagFormInstance,
            formType='editTag');
    
@app.route('/tags/<int:tagID>/delete')
def deleteTagView(tagID):

    selectedTag = Tags.returnTagByID(tagID);
    if not selectedTag:
        return '404';

    selectedTag.deleteTag();
    return redirect(url_for('tagView'));
