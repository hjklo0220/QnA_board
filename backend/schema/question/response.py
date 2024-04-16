from typing import List
import datetime

from pydantic import BaseModel

class AnswerSchema(BaseModel):
    id: int
    question_id: int
    content: str
    author_id: int
    create_date: datetime.datetime
    modify_date: datetime.datetime | None

    class Config:
        from_attributes=True
        orm_mode = True

class QuestionSchema(BaseModel):
    id: int
    subject: str
    content: str
    author_id: int
    create_date: datetime.datetime
    modify_date: datetime.datetime | None
    answers: List[AnswerSchema] = []


    class Config:
        orm_mode = True
        from_attributes=True


class QuestionListSchema(BaseModel):
    total: int
    questions: List[QuestionSchema]

