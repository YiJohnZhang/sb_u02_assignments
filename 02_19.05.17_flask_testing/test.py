from unittest import TestCase;
from app import app;
from flask import session;
from boggle import Boggle;
import json;

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
	def setUp(self):
		''''''

	def tearDown(self):
		''''''

	def test_GETIndex(self):
		with app.test_client() as request:
			response = request.get('/');
			html = response.get_data(as_text=True);

			self.assertEqual(response.status_code, 200);
			self.assertIn('button id=\"reStartGame\"', html);

	def test_POSTIndex(self):
		with app.test_client() as request:
			response = request.post('/', {"boggleWord": "afsd"});
			data = json.loads(response.get_data(as_text=True));

			self.assertEqual(data.result, 'not-on-board');
	
	def test_GETSessionScores(self):
		with app.test_client() as request:
			response = request.get('/endgame');
			data = json.loads(response.get_data(as_text=True));

			self.assertEqual(len(data), 0);

	def test_POSTSessionScores(self):
		with app.test_client() as request:
			response = request.post('/endgame', {"score": 8});
			data = json.loads(response.get_data(as_text=True));

			self.assertIn(data[0]['score'], 8);