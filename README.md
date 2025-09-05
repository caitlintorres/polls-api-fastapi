# FastAPI Polls API (SQLite + SQLAlchemy)

A simple polls API built with FastAPI, SQLite, and SQLAlchemy.  
You can create polls, vote on options, and retrieve poll results.  
The code is written so you can easily switch to PostgreSQL or MySQL later.

---

## Features
- Create polls with multiple options
- Vote for an option
- Retrieve poll details with vote counts
- Uses SQLite by default (easy to run locally)
- ORM powered by SQLAlchemy
- Auto-generated API docs via Swagger UI

---

## Requirements
- Python 3.8+
- pip

---

## Installation

1. Clone the repository
   git clone https://github.com/caitlintorres/polls-api-fastapi.git
   cd polls-api-fastapi

2. Install dependencies
   pip install -r requirements.txt

3. Run the API
   uvicorn main:app --reload

4. Access the docs
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

---

## Project Structure
polls-api-fastapi/
│── main.py           # API routes
│── database.py       # Database connection setup
│── models.py         # SQLAlchemy models
│── schemas.py        # Pydantic schemas
│── polls.db          # SQLite database (auto-created)
│── requirements.txt  # Python dependencies

---

## API Endpoints

### Create a poll
POST /polls/
Request body:
{
  "question": "What's your favorite programming language?",
  "options": [
    {"text": "Python"},
    {"text": "JavaScript"},
    {"text": "Go"}
  ]
}

Response:
{
  "id": 1,
  "question": "What's your favorite programming language?",
  "options": [
    {"id": 1, "text": "Python", "votes": 0},
    {"id": 2, "text": "JavaScript", "votes": 0},
    {"id": 3, "text": "Go", "votes": 0}
  ]
}

---

### Get a poll
GET /polls/{poll_id}  
Example: /polls/1

---

### Vote for an option
POST /polls/{poll_id}/vote/{option_id}  
Example: /polls/1/vote/2

---

## Switching to PostgreSQL or MySQL
Edit SQLALCHEMY_DATABASE_URL in database.py:

# PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

# MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"