from pydantic import BaseModel
from typing import List, Optional

class OptionBase(BaseModel):
    text: str

class OptionCreate(OptionBase):
    pass

class Option(OptionBase):
    id: int
    votes: int

    class Config:
        orm_mode = True

class PollBase(BaseModel):
    question: str

class PollCreate(PollBase):
    options: List[OptionCreate]

class Poll(PollBase):
    id: int
    options: List[Option]

    class Config:
        orm_mode = True
