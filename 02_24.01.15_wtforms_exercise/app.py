from flask import Flask, render_template, redirect, url_for, flash, request;
from flask_debugtoolbar import DebugToolbarExtension;
from models import db, connectDB, Pet;
from forms import PetAddForm, PetEditForm;

app = Flask(__name__);

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sb_24_01_15';
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['SQLALCHEMY_ECHO'] = False;
app.config['SECRET_KEY'] = 'default';

app.debug = True;
toolbar = DebugToolbarExtension(app);
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;

connectDB(app);
db.create_all();

@app.route('/')
def indexView():
    petList = Pet.returnListOfPets();
    return render_template('listPets.html', petList = petList);

@app.route('/add', methods=['GET', 'POST'])
def createPetView():
    
    addPetForm = PetAddForm();

    if addPetForm.validate_on_submit():

        requestFormData = Pet.cleanRequestData(request.form, createPetDefaults = True);

        Pet.createPet(requestFormData);
        flash(f'Created {requestFormData["name"]}!', 'alert alert-success');
        return redirect(url_for('indexView'));
    else:
        return render_template('base.html',
            form = addPetForm, 
            isAddForm = True);

@app.route('/<int:petID>', methods=['GET', 'POST'])
def viewPetView(petID):
    '''Specified to combine both editing and modifying the pet.'''

    selectedPet = Pet.returnPetByID(petID);

    if not selectedPet:
        return '404';

    # inject data
    editPetForm = PetEditForm(**(selectedPet.returnInstanceAttributes()));

    if editPetForm.validate_on_submit():
        # interesting: for the past 3 days, this was never triggered: if editPetForm.validate_on_submit():
            # probably because I hidden the "addForm" features with a hackey way. However, the fact that it kept stating 'db.session.ROLLBACK' misled me to believe this route was being triggered without further deubgging
        
        requestFormData = Pet.cleanRequestData(request.form);

        selectedPet.updatePet(requestFormData);
        flash(f'Successfully edited {selectedPet.name}!', 'alert alert-success');
        return redirect(url_for('indexView'));
    else:
        return render_template('viewPet.html',
            form = editPetForm, 
            selectedPet = selectedPet);