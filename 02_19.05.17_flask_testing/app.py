from boggle import Boggle
from flask import Flask, request, render_template;

boggleGame = Boggle();
boggleBoard = boggleGame.make_board();

app = Flask(__name__);

@app.route('/')
def indexView():
	'''
		Index route.
	'''
	return render_template('boggleGame.html', board=boggleBoard);

@app.route('/', methods=['POST'])
def checkWordView():
	'''
		A route to check the word.
	'''

	submittedWord = request.form['boggleWord'];
	result = Boggle.check_valid_word(boggleBoard, submittedWord)

	if(result == "ok"):
		
		# if(Boggle.find(boggleBoard, submittedWord)):
			# check_valid_word() already calls it.

		return {
			"result": result,
			"word": submittedWord
		};

	return {
		"result": result
	};