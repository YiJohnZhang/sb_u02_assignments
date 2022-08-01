"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy;

db = SQLAlchemy();

def connectDatabase(app):
    db.app = app;
    db.init_app(app);

class Cupcake(db.Model):
    '''Cupcake Model.'''

    __tablename__='cupcake';

    id = db.Column(db.Integer, autoincrement=True, primary_key=True);
    flavor = db.Column(db.String(32), nullable=False);
    size = db.Column(db.Integer, nullable=False);       # FK
    rating = db.Column(db.Float, nullable=False);
    image = db.Column(db.Text, nullable=False, default='https://thestayathomechef.com/wp-content/uploads/2017/12/Most-Amazing-Chocolate-Cupcakes-1-small.jpg');

    def __repr__(self):
        '''Self-representation of Cupcake Model.'''
        return f'<Cupcake {self.id}, {self.flavor} flavor>';

    @classmethod
    def json_serializeModel(cls, modelObject):
        
        modelProperties = vars(modelObject);
        modelProperties.pop('_sa_instance_state');
            # '_sa_instance_state' is a vars() property that stores Object's memory location and is the default SQLAlchemy object __repr__

        return modelProperties;

    @classmethod
    def cleanRequestData(cls, requestData):
        ''''''

        mutableRequestData = dict(requestData);

        if mutableRequestData.get('csrf_token'):
            mutableRequestData.pop('csrf_token');
        
        if mutableRequestData.get('image'):
            if mutableRequestData.get('image') == '':
                mutableRequestData['image'] == None;

        return mutableRequestData;

    @classmethod
    def returnCupcakeList(cls):
        return cls.query.all();

    @classmethod
    def json_returnCupcakeList(cls):
        
        cupcakeList = cls.returnCupcakeList();
        json_cupcakeList = [cls.json_serializeModel(cupcakeInstance) for cupcakeInstance in cupcakeList];
        return json_cupcakeList;
    
    @classmethod
    def returnCupcakeByID(cls, cupcakeID):
        return cls.query.get_or_404(cupcakeID);

    @classmethod
    def filterCupcakesBySearch(cls, searchQuery):
        return;

    @classmethod
    def createCupcake(cls, requestData):

        data = cls.cleanRequestData(requestData);
        newCupcake = Cupcake(**data);

        db.session.add(newCupcake);
        db.session.commit();

        # for some reason this succeeds the test_create_cupcake() in tests.py otherwise it "forgets" there is an id
        # print(newCupcake.id);
        newCupcake = cls.query.get_or_404(newCupcake.id);
            # non-print version to remind lol

        return newCupcake;

    def updateCupcake(self, requestData):

        data = Cupcake.cleanRequestData(requestData);
        db.session.query(Cupcake).filter(Cupcake.id == self.id).update(data);
        db.session.commit();

        return Cupcake.query.get(self.id);

    def deleteCupcake(self):
        db.session.delete(self);
        db.session.commit();
        return "deleted";

class Size(db.Model):
    '''Size Column. Not for external modification.'''

    __tablename__='cupcake_size';

    id = db.Column(db.Integer, autoincrement=True, primary_key=True);
    size_name = db.Column(db.String(8), nullable=False);

    def __repr__(self):
        '''Self-representation of (Cupcake) Size Model.'''
        return f'<Size {self.id}: {self.size_name}>';

    @classmethod
    def returnAllSizes(cls):
        return cls.query.all();