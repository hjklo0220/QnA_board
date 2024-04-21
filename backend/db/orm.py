import datetime

from pydantic import EmailStr
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from schema.question.request import CreateAnswerRequest, CreateQuestionRequest, UpdateQuestionRequest


Base = declarative_base()

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)
    author_id = Column(Integer, ForeignKey("user.id") , nullable=False)
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
    user = relationship("User", backref="question_users")

    def __repr__(self):
        return f"<Question(id={self.id}, subject={self.subject}, content={self.content}), author_id={self.author_id}, create_date={self.create_date}, modify_date={self.modify_date}>"

    @classmethod
    def create(cls, request: CreateQuestionRequest, author_id: int) -> "Question":
        return cls(
            subject=request.subject,
            content=request.content,
            author_id=author_id,
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
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)
    question = relationship(Question, back_populates="answers")
    author_id = Column(Integer, ForeignKey("user.id") , nullable=False)
    user = relationship("User", backref="answer_users")

    def __repr__(self):
        return f"<Answer(id={self.id}, question_id={self.question_id}, content={self.content}), author_id={self.author_id}, create_date={self.create_date}, modify_date={self.modify_date}>"
    
    @classmethod
    def create(
        cls,
        request: CreateAnswerRequest,
        question_id: int,
        author_id: int,
    ) -> "Answer":
        return cls(
            question_id=question_id,
            content=request.content,
            author_id=author_id, # user 모델 완성후 수정
            create_date=datetime.datetime.now(),
            modify_date=None,
        )
    
    def update(self, request: CreateAnswerRequest, answer: "Answer") -> "Answer":
        answer.content = request.content
        answer.modify_date = datetime.datetime.now()
        return answer
    

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    create_date = Column(DateTime, unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, password={self.password}, email={self.email}, create_date={self.create_date}, modify_date={self.modify_date}>"

    @classmethod
    def create(cls, username: str, hashed_password: str, email: EmailStr) -> "User":
        return cls(
            username=username,
            password=hashed_password,
            email=email,
            create_date=datetime.datetime.now(),
        )
