from typing import List
import datetime

from pydantic import BaseModel

class QuestionSchema(BaseModel):
    id: int
    subject: str
    content: str
    author_id: int
    create_date: datetime.datetime
    modify_date: datetime.datetime | None


    class Config:
        orm_mode = True
        from_attributes=True


class QuestionListSchema(BaseModel):
    questions: List[QuestionSchema]

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