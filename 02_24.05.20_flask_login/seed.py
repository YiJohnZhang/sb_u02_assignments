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
    password="$2b$12$AIi5ILgwil59Fg3ANzbJ/e63615dwETElY1q/bbKsHFoGj/MPhI0K",
    email="asdf@asdf.com",
    first_name="asdf",
    last_name="asdf",
);

user2 = User(
    username="jkl",
    password="$2b$12$sC7/46vtuAppAw3jAYVWKOT8yUiB7DdFdVwpTec2Eu7DKR.lrQ2qy",
    email="jklf@asdf.com",
    first_name="jkl",
    last_name="jkl",
);
admin = User(
	username="admin",
	password="$2b$12$KTZXecUAyOWpamDdjzaOZujjuX3Xw3aWTrU0uxDH1qXGbFUFX7yqO",
	email="admin@admin",
	first_name="admin",
	last_name="admin",
	is_admin=True
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

db.session.add_all([user1, user2, admin, feedbackasdf1, feedbackasdf2, feedbackjkl1])
db.session.commit()
