# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

cd backend
env\scripts\activate

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup DONE
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server (WINDOWS)

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Endpoints
### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

### GET '/questions'  
- Fetches a dictionary of questions, number of total questions, current category, categories. 
- Pagination : 10 questions. 
- Request Arguments: None  
- Returns:
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 20
}
 
### DELETE '/questions/<int:question_id>' 
- Delete a question from database by ID and refresh the page
- Request Arguments: question_id  
- Returns: None
  
### POST '/questions'
- Create a new question, which will require the question and answer text, category, and difficulty score.
- Return any questions for whom the search term is a substring of the question.
- Request Arguments : question, answer, difficulty, category, searchTerm
- Returns : questions, categories
   
### GET /categories/<int:category_id>/questions
- Get questions based on category. 
- Request Arguments: category_id  
- Returns:
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": 2, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 5
}

### POST '/quizzes'
- Fetch questions to play the quiz. 
- Request Arguments: category and previous question parameters 
- Returns: a random questions within the given category, 
  if provided, and that is not one of the previous questions. 


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Error handlers
- '404': "resource not found"
- '422': "unprocessable"
- '400': "bad request"


## Other errors

# No application found. Either work inside a view function or push an application context.
https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

# KeyError: 'SQLALCHEMY_TRACK_MODIFICATIONS'
https://stackoverflow.com/questions/45274152/flask-sqlalchemy-keyerror-sqlalchemy-track-modifications

# Handling imports in __init__.py
from backend.models import setup_db, Question, Category