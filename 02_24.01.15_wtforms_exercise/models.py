from flask_sqlalchemy import SQLAlchemy;

db = SQLAlchemy();

def connectDB(app):
    '''Connect to a specified database.'''
    db.app = app;
    db.init_app(app);

class Pet(db.Model):
    '''Pet relation model.'''

    __tablename__ = 'pets';

    id = db.Column(db.Integer, autoincrement = True, primary_key = True);
    name = db.Column(db.String(32), nullable = False);
    species = db.Column(db.String(16), nullable = False);
    age = db.Column(db.Integer, nullable = True);
    photo_url = db.Column(db.String(), nullable = True);
    notes = db.Column(db.Text, nullable = True);
    available = db.Column(db.Boolean, default=bool('True'));

    def __repr__(self):
        '''Self representation of a Pet Instance is: <Pet {id}: {name}>'''
        return f'<Pet {self.id}: {self.name}>';

    def returnInstanceAttributes(self):
        '''Return a dict (kwarg list) of this object's attributes.'''
        # [property for property in dir(selectedPet) if not property.startswith('_')]
            # Hint by Meitham: https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python

        # [for property in dir(self) if not (property.startwith('_') or callable(getattr(self, property)))]; # eliminates all (d)under properties and functions
            # yields 3 'overhead' attributes: 'metadata', 'query', 'registry' if I do the above:
                # self.query yields a `flask_sqlalchemy.BaseQuery` object, i.e. <flask_sqlalchemy.BaseQuery object at 0x7f85855d6790>
                # self.registry yields a `sqlalchemy.orm.decl_api.registry` object, i.e. <sqlalchemy.orm.decl_api.registry object at 0x7f787eab60d0>
                # self.metadata yields a `MetaData()` function
        # get instance attributes fast with `vars()`: https://datagy.io/python-print-objects-attributes/
            # sqlAlchemy has an overhead attribute of '_sa_instance_state', i.e. vars(self) may yield: 
                # {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x7fd33c3a43a0>, 'species': 'Doggo', 'id': 3, 'photo_url': '', 'available': True, 'age': 2, 'name': 'TestChecked', 'notes': ''}
        instanceAttributes = vars(self);
        # instanceAttributes.pop('_sa_instance_state');   # apparently it skips over it, for now
        return instanceAttributes;

    def updatePet(self, data):
        '''Update the selected Pet instance.'''        
        # self.update(**data);  # there is no 'update()' method for the instance
            # https://stackoverflow.com/questions/270879/efficiently-updating-database-using-sqlalchemy-orm
        db.session.query(Pet).filter(Pet.id == self.id).update(data);
        db.session.commit();
        return;

    # def deletePet(self):
    #     db.session.delete(self.id);
    #     db.session.commit();
    #     return;

    @classmethod
    def createPet(cls, data):
        '''Create a new Pet instance.'''
        db.session.add(Pet(**data));    # convert a dict to kwargs: https://stackoverflow.com/questions/5710391/converting-python-dict-to-kwargs
        db.session.commit();
        return;

    @classmethod
    def returnPetByID(cls, petID):
        '''Return a Pet by petID.'''
        return cls.query.get_or_404(petID);
            # `None`python if it DNE
        
    @classmethod
    def returnPetByAvailability(cls):
        '''Return Pet(s) categorized by availability.'''
        return {
            'available': cls.query.filter(cls.available == True),
            'adopted': cls.query.filter(cls.available == False)
        };

    @classmethod
    def returnListOfPets(cls, returnLimit = None, pageNumber = 0):
        '''Return Pet(s), generalized with pagination ( added return limit and page number). Need to integrate filters. (WHERE)'''
        query = cls.query;
        if returnLimit:
            query = query.limit(returnLimit)
        if pageNumber:
            query = query.offset(returnLimit * pageNumber);
        return query.all();

    # @classmethod
    # def sortPetsByDateCreated(cls, sortMethod = "ASC", returnLimit = None):
    #     # returnListOfPets(returnLimit)
    #     return returnListOfPets;
    
    # @classmethod
    # def sortPetsByDistance(cls):
    #     #
    #     return cls.;

    @classmethod
    def cleanRequestData(cls, requestData, createPetDefaults = False):
        '''This is a general helper method to clean request data relating to the Pet object.'''
        mutableRequestData = dict(requestData);

        if mutableRequestData['csrf_token']:
            # remove 'csrf_token' from messing up Pet obj when passing information as **kwarg
            mutableRequestData.pop('csrf_token');
        
        if 'age' in mutableRequestData and not isinstance(mutableRequestData['age'],(int)):
            # added `'age' in requestFormData` for generality. parses `''` as `None` because `''` conflicts with the SQL (NULLABLE) INTEGER constraint
            mutableRequestData['age'] = None;
        
        if not createPetDefaults:
            # if not from a createRoute

            mutableRequestData['available'] = 'available' in mutableRequestData;
                # POST only returns "successful" controls (https://stackoverflow.com/questions/30681482/why-we-cannot-post-unchecked-checkbox), i.e. a checked checkbox is successful, otherwise not
                # DO THIS FOR ALL BOOLEANFIELDS (also radio buttons)
        
        return mutableRequestData;
        


