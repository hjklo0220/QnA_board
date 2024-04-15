import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from schema.question.request import CreateQuestionRequest, UpdateQuestionRequest


Base = declarative_base()

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Question(id={self.id}, subject={self.subject}, content={self.content}), author_id={self.author_id}, create_date={self.create_date}, modify_date={self.modify_date}>"

    @classmethod
    def create(cls, request: CreateQuestionRequest) -> "Question":
        return cls(
            subject=request.subject,
            content=request.content,
            author_id=1, # user 모델 완성후 수정
            create_date=datetime.datetime.now(),
            modify_date=None,
        )
    
    def update(self, request: UpdateQuestionRequest, question: "Question") -> "Question":
        question.subject = request.subject
        question.content = request.content
        question.modify_date = datetime.datetime.now()
        return question


class Answer(Base):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    content = Column(Text, nullable=False)
    author_id = Column(Integer, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)
    question = relationship(Question, backref="answers")

    def __repr__(self):
        return f"<Answer(id={self.id}, question_id={self.question_id}, content={self.content}), author_id={self.author_id}, create_date={self.create_date}, modify_date={self.modify_date}>"