// Game Session Variables
let sessionScore = 0;
let submittedWords = new Set([]);

// Game Application Variables
let gameStarted = false;
let intervalID;
let timer = 60;

// HTMLDOMElements
let submitFormButton;
let feedbackParagraph;
let sessionDatalUL;

const endGame = () => {

	submitFormButton.removeEventListener('click', (evt) => console.log(evt));
	clearInterval(intervalID);

	axios.post('/endgame', {
		'score': sessionScore
	}).then((response) => {

		const {gameSession} = response.data;
		
		sessionDatalUL.innerHTML = '';
		for(let {score, session} of gameSession){

			// console.log(`${session}: ${score}`)
			const newLiElement = document.createElement('li');
			newLiElement.innerText = `Session ${session+1}: ${score} points`;
			sessionDatalUL.appendChild(newLiElement);
			
		}


	}).catch((error) => console.log(error));

}

const keepTrackOfTime = () => {

	timer = timer - 1;
	console.log(`timer: ${timer}; score: ${sessionScore}`);
	
	if(timer < 0)
		endGame();	
		
}

const restartGame = () => {
	
	// Game Session Variables
	sessionScore = 0;
	submittedWords = new Set([]);

	// Game Application Variables
	timer = 60;

}

const allowUserToPlayGame = () => {

	submitFormButton.addEventListener('click', async (evt) => {
		
		evt.preventDefault();

		const submittedWord = document.getElementById('boggleWordInput').value;

		// const response = await axios.post('/', {
		// 	boggleWord: submittedWord
		// });

		axios.post('/', {
			boggleWord: submittedWord
		})
		.then((response) => {

			const {result, word} = response.data;

			if(word && !submittedWords.has(word)){
		
				sessionScore = sessionScore + word.length;
				submittedWords.add(word);

				feedbackParagraph.innerText = `"${word}" accepted!`;

			}else if (word && submittedWords.has(word)){

				// do something to say word already used.

				feedbackParagraph.innerText = `"${word}" is already submitted`;
		
			}else{

				feedbackParagraph.innerText = `"${submittedWord}" rejected: ${result}`;
			}

		})
		.catch((error) => console.log(error));

	});

}

const setupGame = () => {

	submitFormButton = document.getElementById('submitTestWord');
	feedbackParagraph = document.getElementById('submissionFeedback');
	sessionDatalUL = document.getElementById('sessionDetails');

	const reStartGameButton = document.getElementById('reStartGame');
	reStartGameButton.addEventListener('click', (evt) => {

		gameStarted = !gameStarted;

		if(gameStarted){

			intervalID = setInterval(keepTrackOfTime, 1000);
			console.log(intervalID);
			allowUserToPlayGame();

		}else{

			endGame();
			restartGame();

		}

	});

}

window.addEventListener('load', setupGame)