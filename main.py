from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/polls/", response_model=schemas.Poll)
def create_poll(poll: schemas.PollCreate, db: Session = Depends(get_db)):
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

@app.get("/polls/{poll_id}", response_model=schemas.Poll)
def get_poll(poll_id: int, db: Session = Depends(get_db)):
    db_poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    if not db_poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return db_poll

@app.post("/polls/{poll_id}/vote/{option_id}", response_model=schemas.Poll)
def vote_poll(poll_id: int, option_id: int, db: Session = Depends(get_db)):
    db_option = db.query(models.Option).filter(
        models.Option.id == option_id, models.Option.poll_id == poll_id
    ).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    db_option.votes += 1
    db.commit()
    return db.query(models.Poll).filter(models.Poll.id == poll_id).first()
