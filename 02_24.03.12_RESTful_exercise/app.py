"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template, abort;
from models import db, connectDatabase, Cupcake, Size;
from forms import CupcakeForm;
from flask_debugtoolbar import DebugToolbarExtension;
from secret import API_SECRET_KEY;              # replace this when testing locally


app = Flask(__name__);

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sb_24.03.12';
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['SQLALCHEMY_ECHO'] = False;
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
app.config['SECRET_KEY'] = API_SECRET_KEY;              # replace this when testing locally

toolbar = DebugToolbarExtension(app); 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;

connectDatabase(app);
db.create_all();

# Front-End
@app.route('/')
def indexView():
    
    cupcakeForm = CupcakeForm();
    cupcakeForm.size.choices=[(choice.id, choice.size_name) for choice in Size.returnAllSizes()]

    return render_template('form.html', form = cupcakeForm);

# API
@app.route('/api/cupcakes')
def returnCupcakesView():
    return jsonify(cupcakes=Cupcake.json_returnCupcakeList());

@app.route('/api/cupcakes/<int:cupcakeID>')
def returnCupcakeView(cupcakeID):

    selectedCupcake = Cupcake.returnCupcakeByID(cupcakeID);
    if not selectedCupcake:
        abort(404);
    
    return jsonify(cupcake=Cupcake.json_serializeModel(selectedCupcake));

@app.route('/api/cupcakes', methods=['POST'])
def newCupcakeView():

    # render form in a different route (hehe, guessed s5)
        # newCupcakeForm = CupcakeForm();

        # if newCupcakeForm.validate_on_submit():

        #     Cupcake.createCupcake(request.form)
        #     return jsonify(cupcake=Cupcake.)
        
        # else:
        #     return render_template('', form=newCupcakeForm)
    # jsonify data after processing
    # pass the data to the post field

    newCupcake = Cupcake.createCupcake(request.form)

    return (jsonify(cupcake=Cupcake.json_serializeModel(newCupcake)), 201);

@app.route('/api/cupcakes/<int:cupcakeID>', methods=['PATCH'])
def patchCupcakeView(cupcakeID):
    
    selectedCupcake = Cupcake.returnCupcakeByID(cupcakeID);
    if not selectedCupcake:
        abort(404);

    updateCupcake = selectedCupcake.updateCupcake(request.json);

    return jsonify(cupcake=Cupcake.json_serializeModel(updateCupcake));

@app.route('/api/cupcakes/<int:cupcakeID>', methods=['DELETE'])
def deleteCupcakeView(cupcakeID):

    selectedCupcake = Cupcake.returnCupcakeByID(cupcakeID);
    if not selectedCupcake:
        abort(404);
    
    return jsonify(message=selectedCupcake.deleteCupcake());


@app.errorhandler(404)
def error_404_view(error):
    return ('404', 404);
