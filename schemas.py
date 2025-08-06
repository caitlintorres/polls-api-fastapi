from pydantic import BaseModel
from typing import List

class OptionCreate(BaseModel):
    text: str

class PollCreate(BaseModel):
    question: str
    options: List[OptionCreate]

class Option(BaseModel):
    id: int
    text: str
    votes: int

class Poll(BaseModel):
    id: int
    question: str
    options: List[Option]
