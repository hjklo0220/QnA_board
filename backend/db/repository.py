from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_

from db.connection import get_db
from db.orm import Question, Answer, User, question_voter


class QuestionRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def vote_question(self, question_id: int, user_id: int) -> None:
        question: Question = self.session.scalar(select(Question).where(Question.id == question_id))
        user: User = self.session.scalar(select(User).where(User.id == user_id))
        if question and user:
            # question.voter에 user가 있는지 확인
            if user in question.voter:
                question.voter.remove(user)
            else:
                question.voter.append(user)
        self.session.commit()

    def get_question_list(self, page_number: int, page_size: int, keyword: str = "") -> tuple:
        # 페이징 정보
        # page_number = 1  # 페이지 번호
        # page_size = 10   # 페이지 당 아이템 수

        offset = page_number*page_size
        _question_list = (
            self.session.query(Question)
            .order_by(Question.create_date.desc())
        )
        if keyword:
            search = "%{}%".format(keyword)
            sub_query = self.session.query(Answer.question_id, Answer.content, User.username)\
                .outerjoin(User, and_(Answer.author_id == User.id)).subquery()
            _question_list = _question_list \
                .outerjoin(User) \
                .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id)) \
                .filter(Question.subject.ilike(search) |
                        Question.content.ilike(search) |
                        User.username.ilike(search) |
                        sub_query.c.content.ilike(search) |
                        sub_query.c.username.ilike(search)
                        )
        
        total: int = _question_list.count()
        question_list = _question_list.offset(offset).limit(page_size).all()
        return total, question_list
    
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

    def vote_answer(self, answer_id: int, user_id: int) -> None:
        answer: Answer = self.session.scalar(select(Answer).where(Answer.id == answer_id))
        user: User = self.session.scalar(select(User).where(User.id == user_id))

        if answer and user:
            if user in answer.voter:
                answer.voter.remove(user)
            else:
                answer.voter.append(user)

        self.session.commit()

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

class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_existing_user(self, username: str) -> User | None:
        return self.session.scalar(select(User).where(User.username == username))
    
    def get_user(self, username: int) -> User:
        return self.session.scalar(select(User).where(User.username == username))

    def save_user(self, user: User) -> User:
        self.session.add(instance=user)
        self.session.commit()
        self.session.refresh(instance=user)
        return user