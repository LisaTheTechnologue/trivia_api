import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origins','*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')    
    return response

  # viewAllCategories
  @app.route("/categories")
  def get_categories():
    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}
    return jsonify({'success': True,
                    'categories': formatted_categories
                    })

  # view questions
  @app.route("/questions", methods=['GET'])
  def get_questions():
    selection = Question.query.all()
    current_questions = paginate_questions(request,selection)
    
    if len(current_questions) == 0:
      abort(404)

    categories = Category.query.all()
    # formatted_categories = [question.format() for question in selection]
    formatted_categories = []
    for c in categories:
      formatted_categories.append(c.type)
    return jsonify({
        'success':True,
        'questions': current_questions,
        'categories':formatted_categories,
        'total_questions': len(selection)
        })

  # delete question
  @app.route("/questions/<int:question_id>", methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'total_questions': len(selection)
      })

    except:
      abort(422)
  
  # FormView / submitQuestion + searchQuestion
  @app.route("/questions", methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question',None)
    new_answer = body.get('answer',None)
    new_difficulty = body.get('difficulty',None)
    new_category = body.get('category',None)
    search = body.get('searchTerm',None)
        
    try:
      if search:
        
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        current_questions = paginate_questions(request,selection)
        
        return jsonify({'success':True,
                    'questions':current_questions,
                    'total_questions': len(selection.all())
                    })
      else:
        question = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request,selection)
        
        return jsonify({'success':True,
                        'created':question.id,
                        'questions':current_questions,
                        'total_questions': len(selection)
                        })

    except:
      abort(422)

  # QuestionView / viewQbyC
  @app.route("/categories/<int:category_id>/questions")
  def get_questions_by_category(category_id):
    try:
      category_id = category_id + 1
      selection = Question.query.filter(Question.category==category_id).all()
     
      categories = Category.query.all()
      # formatted_categories = [question.format() for question in selection]
      formatted_categories = []
      for c in categories:
        formatted_categories.append(c.type)
      current_questions = paginate_questions(request,selection)
      return jsonify({
                      'success':True,
                      'questions': current_questions,
                      'categories':formatted_categories,
                      'current_category': category_id,
                      'total_questions': len(selection)
                      })
    except BaseException:
            abort(422)

  # Quiz view
  @app.route("/quizzes", methods=['GET','POST'])
  def play_trivia():
    body = request.get_json()
    if not body:
        abort(400)
    previous_q = body['previous_questions']
    category_id = body['quiz_category']['id']
    category_id = str(int(category_id))

    # select ALL
    if category_id == "0":
      if previous_q is not None:
        questions = Question.query.filter(
            Question.id.notin_(previous_q)).all()
      else:
        questions = Question.query.all()
    else:
      if previous_q is not None:
        questions = Question.query.filter(
            Question.id.notin_(previous_q),
            Question.category == category_id).all()
      else:
        questions = Question.query.filter(
            Question.category == category_id).all()

    if not questions: # empty list
      next_question = False
    else:
      next_question = random.choice(questions).format()

    return jsonify({
        'success': True,
        'question': next_question
    })

  # errors handler
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
  return app

    