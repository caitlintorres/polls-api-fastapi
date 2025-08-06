from fastapi import FastAPI, HTTPException
from typing import List
from schemas import PollCreate, Poll, Option
import models

app = FastAPI()

@app.post("/polls", response_model=Poll)
def create_poll(poll_data: PollCreate):
    global models.option_counter
    poll_id = models.poll_counter
    options = []
    for opt in poll_data.options:
        options.append(Option(id=models.option_counter, text=opt.text, votes=0))
        models.option_counter += 1

    poll = Poll(id=poll_id, question=poll_data.question, options=options)
    models.polls[poll_id] = poll
    models.poll_counter += 1
    return poll

@app.get("/polls", response_model=List[Poll])
def get_polls():
    return list(models.polls.values())

@app.get("/polls/{poll_id}", response_model=Poll)
def get_poll(poll_id: int):
    if poll_id not in models.polls:
        raise HTTPException(status_code=404, detail="Poll not found")
    return models.polls[poll_id]

@app.post("/polls/{poll_id}/vote")
def vote(poll_id: int, option_id: int):
    if poll_id not in models.polls:
        raise HTTPException(status_code=404, detail="Poll not found")

    poll = models.polls[poll_id]
    for option in poll.options:
        if option.id == option_id:
            option.votes += 1
            return {"message": "Vote recorded"}
    raise HTTPException(status_code=404, detail="Option not found")

@app.delete("/polls/{poll_id}")
def delete_poll(poll_id: int):
    if poll_id not in models.polls:
        raise HTTPException(status_code=404, detail="Poll not found")
    del models.polls[poll_id]
    return {"message": "Poll deleted"}
