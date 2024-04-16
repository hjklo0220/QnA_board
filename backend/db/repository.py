from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from db.connection import get_db
from db.orm import Question, Answer


class QuestionRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_question_list(self) -> List[Question]:
        return list(self.session.scalars(select(Question)))
    
    def get_question_by_id(self, question_id: int) -> Question:
        return self.session.scalar(select(Question).where(Question.id == question_id))

    def create_question(self, question: Question) -> Question:
        self.session.add(instance=question)
        self.session.commit()
        self.session.refresh(instance=question)
        return question
    
    def update_question(self, question: Question) -> Question:
        self.session.add(instance=question)
        self.session.commit()
        self.session.refresh(instance=question)
        return question
    
    def delete_question(self, question: Question) -> None:
        # self.session.execute(delete(Question).where(id == question.id))
        self.session.delete(instance=question)
        self.session.commit()

class AnswerRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_answer_list_by_question(self, question_id: int) -> List[Answer]:
        return list(self.session.scalars(select(Answer).where(Answer.question_id == question_id)))
    
    def get_answer_by_answer_id(self, answer_id: int) -> Answer:
        return self.session.scalar(select(Answer).where(Answer.id == answer_id))

    def create_answer(self, answer: Answer) -> Answer:
        self.session.add(instance=answer)
        self.session.commit()
        self.session.refresh(instance=answer)
        return answer
    
    def update_answer(self, answer: Answer) -> Answer:
        self.session.add(instance=answer)
        self.session.commit()
        self.session.refresh(instance=answer)
        return answer
    
    def delete_answer(self, answer: Answer) -> None:
        self.session.delete(instance=answer)
        self.session.commit()