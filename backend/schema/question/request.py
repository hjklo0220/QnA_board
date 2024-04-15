from pydantic import BaseModel

class CreateQuestionRequest(BaseModel):
    subject: str
    content: str

class UpdateQuestionRequest(BaseModel):
    subject: str
    content: str

