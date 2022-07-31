from unittest import TestCase;
from app import app;
from models import db, Users;

# Configuration changes
app.config['SQLALCHEMY_DATABSE_URI'] = 'postgresql:///blogly_test';
app.config['SQLALCHEMY_ECHO'] = False;
app.config['SECRET_KEY'] = 'wtf';

# Make Flask errors real errors
app.config['TESTING'] = True;

# Don't clog HTML with Flask Toolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar'];

app.config['WTF_CSRF_ENABLE'] = False;

db.drop_all();
db.create_all();

class AppViewTest(TestCase):
    
    def setUp(self):
        testUser = Users(first_name='Test', last_name='Subject', image_url='');
        db.session.add(testUser);
        db.session.commit();
    
    def tearDown(self):
        db.session.rollback();

    def test_usersView(self):
        with app.test_client() as client:
            response = client.get('/users', follow_redirects=True);
            html = response.get_data(as_text = True);

            self.assertEqual(response.status_code, 200);
            self.assertIn('Subject, Test</a></li>', html);
 
    def test_newUserForm(self):
        with app.test_client() as client:
            response = client.get('/users/new');
            html = response.get_data(as_text = True);

            self.assertEqual(response.status_code, 200);
            self.assertIn('<label for="firstName">First Name</label>', html);

    def test_testUserView(self):
        with app.test_client() as client:
            response = client.get('/users/1');
            html = response.get_data(as_text = True);

            self.assertEqual(response.status_code, 200);
            self.assertIn('<h1>Test Subject</h1>', html);
 
    def test_editUserForm(self):
        with app.test_client() as client:
            response = client.get('/users/1/edit');
            html = response.get_data(as_text = True);

            self.assertEqual(response.status_code, 200);
            self.assertIn('<input id="firstName" name="firstName" required type="text" value="Test">', html);