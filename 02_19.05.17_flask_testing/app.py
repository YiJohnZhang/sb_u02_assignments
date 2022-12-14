from boggle import Boggle;
from flask import Flask, request, render_template;

boggleGame = Boggle();
boggleBoard = boggleGame.make_board();
gameSession = [];

app = Flask(__name__);

@app.route('/', methods=['GET'])
def indexView():
	'''
		Index route.
	'''

	return render_template('boggleGame.html', boggleBoard=boggleBoard);

@app.route('/', methods=['POST'])
def checkWordView():
	'''
		A route to check the word.
	'''

	# print(request.data.decode('utf-8'));
	# print(request.data.decode('utf-8').split(":")[1].strip("}"));
	# asdf = request.data.decode('utf-8').split(":")[1].strip("}").strip('\"')
	# print(asdf);

	# print(request.data.boggleWord)
	# print(request.data["boggleWord"])
	submittedWord = request.data.decode('utf-8').split(':')[1].strip('}').strip('\"');
		# because I didn't submit the form literally, it is passed in the request body
	result = boggleGame.check_valid_word(boggleBoard, submittedWord);

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

@app.route('/endgame', methods=['GET', 'POST'])
def postScoreView():
	'''
		A route to fetch and post the game end score.
	'''

	if(request.method == 'POST'):

		submittedScore = request.data.decode('utf-8').split(':')[1].strip('}').strip('\"');
		print(submittedScore)

		gameSession.append({
			"session": len(gameSession),
			"score": submittedScore
		});

		return {
			"gameSession": gameSession
		};
	
	return {"gamesession": gameSession}