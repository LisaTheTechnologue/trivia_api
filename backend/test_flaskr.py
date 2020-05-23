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
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','password','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is your name?',
            'answer': 'My name is Jolisa',
            'difficulty': 1,
            'category': 1
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

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000',json={'difficulty':1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
        
    def test_delete_question(self):
        insert_res = self.client().post('/questions', json=self.new_question)
        insert_data = json.loads(insert_res.data)
        question_id = insert_data['created']

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_422_if_book_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 3).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')
        
    def test_create_new_question(self):
        res = self.client().post('/questions',json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
            
    def test_search_questions_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'burton'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)
        self.assertTrue(data['total_questions'])

    def test_search_questions_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'michigan'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)

    def test_get_questions_in_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 4)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], '4')

    def test_get_quiz_questions_with_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': [],
                                                   'quiz_category': {'id': '1'}
                                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'], True)


    def test_get_quiz_questions_all_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': [],
                                                   'quiz_category': {'id': '0'}
                                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()