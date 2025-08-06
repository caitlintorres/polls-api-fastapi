# 🗳️ FastAPI Polls API

A simple backend project built with **FastAPI** that allows users to create polls, vote on options, and view results. This project is perfect for practicing REST API design and in-memory data storage using Python.

---

## 🚀 Features

- ✅ Create a poll with multiple options
- ✅ Vote on an option
- ✅ View all polls
- ✅ View a single poll with vote counts
- ✅ Delete a poll

---

## 🛠 Tech Stack

- **Language**: Python 3.8+
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Storage**: In-memory (no database)

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

Start the development server:

```bash
uvicorn main:app --reload
```

Visit the interactive API docs at:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📁 Project Structure

```
polls_api_fastapi/
├── main.py          # FastAPI app and endpoints
├── models.py        # In-memory data store
├── schemas.py       # Pydantic schemas
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

---

## 📬 Example API Usage

### Create a Poll
```http
POST /polls
```

**Body:**
```json
{
  "question": "What's your favorite language?",
  "options": [
    { "text": "Python" },
    { "text": "JavaScript" }
  ]
}
```

### Vote on a Poll
```http
POST /polls/{poll_id}/vote?option_id={option_id}
```

---

## 🧠 Learning Concepts

This project demonstrates:

- FastAPI basics
- Routing and endpoint creation
- Data validation with Pydantic
- Simple state management with in-memory Python structures
- Interactive API documentation with Swagger

---

## 🔄 Future Improvements

- Persistent storage with SQLite or PostgreSQL
- User authentication
- Poll expiration and visibility settings
- Pagination for large poll sets

---

## 🧑‍💻 Author

Made with ❤️ using FastAPI.
