import os
from re import T
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # CORS(app)
    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/categories')
    def retrieve_categories():
        categories = {}

        for category in Category.query.all():
            all_categories = {
                category.id: category.type
            }
            categories.update(all_categories)

        return jsonify({
            'categories': categories
        })

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route('/questions')
    def retrieve_questions():
        categories = {}

        for category in Category.query.all():
            all_categories = {
                category.id: category.type
            }
            categories.update(all_categories)
        
        page = request.args.get('page', 1, type=int)
        questions= Question.query.paginate(page, per_page=QUESTIONS_PER_PAGE)  
        formatted_questions = [professor.format() for professor in questions.items]

        return jsonify({
            'questions': formatted_questions,
            'totalQuestions': len(Question.query.all()),
            'categories': categories
        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
        except:
            abort(404)

        return jsonify({
            "success": True
        })

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            question = Question(question=new_question, answer=new_answer,
                                difficulty=new_difficulty, category=new_category)
            question.insert()
        except:
            abort(422)

        return jsonify({
            "success": True
        })
    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        categories = {}
        body = request.get_json()
        search_term = body.get('searchTerm')

        for category in Category.query.all():
            all_categories = {
                category.id: category.type
            }
            categories.update(all_categories)

        page = request.args.get('page', 1, type=int)
        questions= Question.query.filter(Question.question.ilike('%'+search_term+'%')).paginate(page, per_page=QUESTIONS_PER_PAGE)  
        formatted_questions = [professor.format() for professor in questions.items]

        return jsonify({
            'questions': formatted_questions,
            'totalQuestions': len(Question.query.all()),
            'categories': categories
        })

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions')
    def questions_by_category(category_id):
        categories = {}

        for category in Category.query.all():
            all_categories = {
                category.id: category.type
            }
            categories.update(all_categories)

        currentCategory = Category.query.filter(
            Category.id == category_id).one_or_none()

        page = request.args.get('page', 1, type=int)
        questions = Question.query.filter(Question.category == category_id).paginate(page, per_page=QUESTIONS_PER_PAGE)  
        formatted_questions = [question.format() for question in questions.items]
        
        if questions.total==0:
          abort(404)

        return jsonify({
            'questions': formatted_questions,
            'totalQuestions': len(Question.query.all()),
            'categories': categories,
            'currentCategory': currentCategory.type
        })

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/quizzes', methods=['POST'])
    def create_quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_question = body.get('previous_questions')

        if(quiz_category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                Question.category == quiz_category['id']).all()

        question = random.choice(questions).format()
        while(question['id'] in previous_question):
            question = random.choice(questions).format()
            if (len(questions) == len(previous_question)):
                return jsonify({
                    'success': True
                })

        return jsonify({
            'question': question
        })
    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app
