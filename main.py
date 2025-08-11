from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------- API ROUTES -----------

@app.post("/api/polls/", response_model=schemas.Poll)
def create_poll_api(poll: schemas.PollCreate, db: Session = Depends(get_db)):
    db_poll = models.Poll(question=poll.question)
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)

    for option in poll.options:
        db_option = models.Option(text=option.text, poll_id=db_poll.id)
        db.add(db_option)
    db.commit()
    db.refresh(db_poll)
    return db_poll

@app.get("/api/polls/{poll_id}", response_model=schemas.Poll)
def get_poll_api(poll_id: int, db: Session = Depends(get_db)):
    db_poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if not db_poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return db_poll

@app.post("/api/polls/{poll_id}/vote/{option_id}", response_model=schemas.Poll)
def vote_poll_api(poll_id: int, option_id: int, db: Session = Depends(get_db)):
    db_option = db.query(models.Option).filter(
        models.Option.id == option_id, models.Option.poll_id == poll_id
    ).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    db_option.votes += 1
    db.commit()
    return db.query(models.Poll).filter(models.Poll.id == poll_id).first()

# ----------- FRONTEND ROUTES -----------

@app.get("/", response_class=HTMLResponse)
def read_index(request: Request, db: Session = Depends(get_db)):
    polls = db.query(models.Poll).all()
    return templates.TemplateResponse("index.html", {"request": request, "polls": polls})
    
@app.get("/polls/new", response_class=HTMLResponse)
def new_poll_form(request: Request):
    return templates.TemplateResponse("new_poll.html", {"request": request})

@app.post("/polls/new")
def create_poll_form(
    request: Request,
    question: str = Form(...),
    options: List[str] = Form(...),
    db: Session = Depends(get_db),
):
    if not question or not options:
        return templates.TemplateResponse(
            "new_poll.html",
            {"request": request, "error": "Please provide a question and at least one option."},
        )
    db_poll = models.Poll(question=question)
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)

    for option_text in options:
        db_option = models.Option(text=option_text, poll_id=db_poll.id)
        db.add(db_option)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/polls/{poll_id}", response_class=HTMLResponse)
def get_poll_page(request: Request, poll_id: int, db: Session = Depends(get_db)):
    db_poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if not db_poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return templates.TemplateResponse("poll.html", {"request": request, "poll": db_poll})

@app.post("/polls/{poll_id}/vote")
def vote_poll_form(poll_id: int, option_id: int = Form(...), db: Session = Depends(get_db)):
    db_option = db.query(models.Option).filter(
        models.Option.id == option_id, models.Option.poll_id == poll_id
    ).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    db_option.votes += 1
    db.commit()
    return RedirectResponse(url=f"/polls/{poll_id}", status_code=303)

