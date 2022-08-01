from app import app
from models import db, Cupcake, Size

# The following code responsible for setting up the database:
# connectDatabase(app);
# db.create_all();

db.init_app(app);

with app.app_context():
    db.drop_all();
    db.create_all();

c1 = Cupcake(
    flavor="cherry",
    size=3,
    rating=5,
)

c2 = Cupcake(
    flavor="chocolate",
    size=1,
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)

size_small = Size(size_name='small');   # 1
size_medium = Size(size_name='medium'); # 2
size_large = Size(size_name='large');   # 3

db.session.add_all([c1, c2, size_small, size_medium, size_large])
db.session.commit()