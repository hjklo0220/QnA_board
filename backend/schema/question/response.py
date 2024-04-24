from typing import List
import datetime

from pydantic import BaseModel

from schema.user.response import UserSchema

class AnswerSchema(BaseModel):
    id: int
    question_id: int
    content: str
    author_id: int
    create_date: datetime.datetime
    modify_date: datetime.datetime | None
    user: UserSchema | None

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
    user: UserSchema | None
    voter: List[UserSchema]


    class Config:
        orm_mode = True
        from_attributes=True


class QuestionListSchema(BaseModel):
    total: int
    question_list: List[QuestionSchema]


class QuestionVoteSchema(BaseModel):
    question_id: int