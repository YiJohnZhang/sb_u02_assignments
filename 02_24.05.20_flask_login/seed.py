from app import app;
from models import db, User, Feedback;

# The following code responsible for setting up the database:
# connectDatabase(app);
# db.create_all();

db.init_app(app);

with app.app_context():
    db.drop_all();
    db.create_all();

user1 = User(
    username="asdf",
    password="asdf",
    email="asdf@asdf.com",
    first_name="asdf",
    last_name="asdf",
);

user2 = User(
    username="jkl",
    password="jkl",
    email="jklf@asdf.com",
    first_name="jkl",
    last_name="jkl",
);

feedbackasdf1 = Feedback(
    title="asdf's First Post",
    content='fasdadfsasdfaaa',
    author='asdf'
);
feedbackasdf2 = Feedback(
    title="fasdadfs",
    content='asjfdadfadsf',
    author='asdf'
)
feedbackjkl1 = Feedback(
    title="jkl's first post",
    content='jklasdfljkasdfklj',
    author='jkl'
)

db.session.add_all([user1, user2, feedbackasdf1, feedbackasdf2, feedbackjkl1])
db.session.commit()
