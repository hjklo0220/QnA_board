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


class QuestionListSchema(BaseModel):
    questions: List[QuestionSchema]