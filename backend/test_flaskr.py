import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:123@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            'question': 'Whats your name?',
            'answer': 'ziyad',
            'difficulty': 1,
            'category': 3
        }
        self.new_quiz = {
            'previous_questions':[20, 21],
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # get categories test
    def test_get_categories(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)

    def test_get_categories_not_found(self):
        res = self.client().get('/categories/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # get questions test
    def test_get_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #  Delete question test //remove comment to test it//
    # def test_delete_question(self):
    #     res = self.client().delete('/questions/33')

    #     question = Question.query.filter(Question.id == 33).one_or_none()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(question, None)

    def test_delete_question_not_found(self):
        res = self.client().delete('/questions/330')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # POST a new question test
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        self.assertEqual(res.status_code, 200)

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    #  questions search test
    def test_search_questions(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'Who'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(len(data['questions']), 3)

    
    def test_get_questions_search_without_results(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'Ziyad'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 0)

    # get questions based on category
    # def test_get_questions_based_on_category(self):
    #     res = self.client().get('/categories/3/questions')
    #     # data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
        # self.assertEqual(data['success'], True)

        # self.assertEqual(data['currentCategory'], 'Art')

    # post quiz test
    # def test_create_quiz(self):
    #     res = self.client().post('/quizzes', json=self.new_quiz)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()