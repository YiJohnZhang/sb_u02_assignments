from unittest import TestCase;
from app import app;
from models import db, Users, Posts;

# Configuration changes
app.config['SQLALCHEMY_DATABSE_URI'] = 'postgresql:///blogly_test';
app.config['SQLALCHEMY_ECHO'] = False;
app.config['SECRET_KEY'] = 'wtf';

# Make Flask errors real errors
app.config['TESTING'] = True;

# Don't clog HTML with Flask Toolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar'];

app.config['WTF_CSRF_ENABLE'] = False;

class AppViewTest(TestCase):
    
    def setUp(self):
        db.create_all();
        testUserOne = Users(first_name='Caroline', last_name='Sweet', image_url='');
        testUserTwo = Users(first_name='Carolijn', last_name='Sweet', image_url='');
        testUserThree = Users(first_name='Test', last_name='Subject', image_url='');
        db.session.add(testUserOne);
        db.session.add(testUserTwo);
        db.session.add(testUserThree);

        testPostOne = Posts(title='Sweet Caroline', content='bang bang bang.', author_id='2');
        testPostTwo = Posts(title='Sweet Carolijn', content='windmill.', author_id='2');
        testPostThree = Posts(title='Dankus', content='Memeus', author_id='2');
        testPostFour = Posts(title='Test', content='Post', author_id='3');
        db.session.add(testPostOne);
        db.session.add(testPostTwo);
        db.session.add(testPostThree);
        db.session.add(testPostFour);

        db.session.commit();

    
    def tearDown(self):
        db.drop_all();

    def test_usersView(self):
        with app.test_client() as client:
            response = client.get('/users', follow_redirects=True);
            html = response.get_data(as_text = True);

            self.assertEqual(response.status_code, 200);
            self.assertIn('Sweet, Carolijn</a></li>', html);
 
    def test_newUserFormView(self):
        with app.test_client() as client:
            response = client.get('/users/new');
            html = response.get_data(as_text = True);

            self.assertEqual(response.status_code, 200);
            self.assertIn('<label for="firstName">First Name</label>', html);

    def test_userView(self):
        with app.test_client() as client:
            response = client.get('/users/2');
            html = response.get_data(as_text = True);

            # some general HTML
            self.assertEqual(response.status_code, 200);
            self.assertIn('<h1>Carolijn Sweet</h1>', html);

            # posts
            self.assertIn('<li><a href="/posts/2">Sweet Carolijn</a>', html)
    
 
    def test_editUserFormView(self):
        with app.test_client() as client:
            response = client.get('/users/2/edit');
            html = response.get_data(as_text = True);

            self.assertEqual(response.status_code, 200);
            self.assertIn('<input id="firstName" name="firstName" required type="text" value="Carolijn">', html);
    
    def test_postView(self):
        with app.test_client() as client:
            response = client.get('/posts/2');
            html = response.get_data(as_text = True);

            self.assertEqual(response.status_code, 200);
            self.assertIn('<h1>Sweet Carolijn', html);
            self.assertIn('<p>windmill', html);
            self.assertIn('<em>By <a href="/users/2">', html);
    
    def test_deletePost(self):
        with app.test_client() as client:
            response = client.get('/posts/2/delete', follow_redirects = True);
            response = client.get('/users/2/', follow_redirects = True);

            self.assertEqual(response.status_code, 404);

    def test_cascadePostDelete(self):
        with app.test_client() as client:
            response = client.get('/users/2/delete', follow_redirects = True);
            response2 = client.get('/posts/1', follow_redirects = True);
            self.assertEqual(response2.status_code, 404);

            response3 = client.get('/posts/2', follow_redirects = True);
            self.assertEqual(response3.status_code, 404);

            response4 = client.get('/posts/3', follow_redirects = True);
            self.assertEqual(response4.status_code, 404);

            response5 = client.get('/posts/4', follow_redirects = True);
            html = response5.get_data(as_text = True);
            self.assertEqual(response5.status_code, 200);
            self.assertIn('<p>Post</p>',html);