from pydantic import BaseModel, field_validator
class CreateQuestionRequest(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('not empty')
        return v

class UpdateQuestionRequest(BaseModel):
    subject: str
    content: str

class CreateAnswerRequest(BaseModel):
    content: str

    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('not empty')
        return v
    
class QuestionVoteRequest(BaseModel):
    question_id: int

class AnswerVoteRequest(BaseModel):
    answer_id: int