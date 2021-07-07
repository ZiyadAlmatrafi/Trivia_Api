### Getting Started:
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

### Error Handling:
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable  


### Endpoints:

# Get Catogaries
Method:GET `http://127.0.0.1:5000/categories`

Get all available categories
- Returns:
```
{
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
}
```
# Get questions
Method:GET `http://127.0.0.1:5000/questions`
Get all available questions, or use `http://127.0.0.1:5000/questions?page=2` to get a specific page.
- Returns:
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```
# Delete a question
Method:DELETE `http://127.0.0.1:5000/questions/<int:question_id>`
Deletes a specified question using the id of the question

# Create a question
Method:POST `http://127.0.0.1:5000/questions`
Sends a post request in order to add a new question
- Request Body:
```
{
    'question':  'Whats your name',
    'answer':  'Ziyad',
    'difficulty': 1,
    'category': 3,
}
```

# Search questions
Method:POST `http://127.0.0.1:5000/questions/search`
- Sends a post request in order to search for a specific question by search term 
- Request Body:
``` 
{
    'searchTerm': 'this is the term the user is looking for'
}
```
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
```
# Get questions based on category
Method:GET `http://127.0.0.1:5000/categories/<int:category_id>/questions`
To get all questions under a category
- Returns:
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}
```

# Play quiz
Method:POST `http://127.0.0.1:5000/quizzes`
- Sends a post request in order to get the next question 
- Request Body: 
```
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
```
- Returns: a single new question object 
```
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}



