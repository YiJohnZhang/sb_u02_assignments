// Game Session Variables
let sessionScore = 0;
let submittedWords = new Set([]);

// Game Application Variables
let gameplayCount = 0;	//s6, delete
let gameStarted = false;
let timer = 60;

const restartGame = () => {
	
	// Game Session Variables
	sessionScore = 0
	submittedWords = new Set([]);

	// Game Application Variables
	gameStarted = !gameStarted;
	timer = 60;

}

const allowUserToPlayGame = () => {

	const submitFormButton = document.getElementById('submitTestWord');
	submitFormButton.addEventListener('click', (evt) => {
		
		evt.preventDefault();
		// axios post call

		const {result, word} = /*...*/;

		if(word && !submittedWords.has(word)){
		
			sessionScore = sessionScore + word.length;
			submittedWords.add(word);

		}else if (word && submittedWords.has(word)){

			// do something to say word already used.
		
		}

	});

}

const setupGame = () => {

	const reStartGameButton = document.getElementById('reStartGame');
	reStartGameButton.addEventListener('click', (evt) => {

		restartGame();

		if(gameStarted){

			allowUserToPlayGame();
			// timer countdown (step5)

		}else{

			submitFormButton.removeEventListener('click');
			// 

		}

	});

}

document.addEventListener('load', setupGame)