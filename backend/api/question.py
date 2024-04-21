from typing import List

from fastapi import APIRouter, Depends, HTTPException

from db.repository import QuestionRepository, UserRepository
from db.orm import Question, User
from schema.question.response import QuestionListSchema, QuestionSchema
from schema.question.request import CreateQuestionRequest
from security import get_access_token
from service.user import UserService


router = APIRouter(prefix="/question")

@router.get("/list", status_code=200)
def get_questions_handler(
    page: int = 0,
    size: int = 10,
    question_repo: QuestionRepository = Depends(),
) -> QuestionListSchema:
    total, question_list= question_repo.get_question_list(page_number=page, page_size=size)
    
    return QuestionListSchema(total=total, question_list=question_list)

@router.get("/{question_id}", status_code=200)
def get_question_handler(
    question_id: int,
    question_repo: QuestionRepository = Depends(),
) -> QuestionSchema:
    question: Question = question_repo.get_question_by_id(question_id)

    if question:
        return QuestionSchema.from_orm(question)
    raise HTTPException(status_code=404, detail="Question not found")

@router.post("/create", status_code=201)
def create_question_handler(
    request: CreateQuestionRequest,
    access_token: str = Depends(get_access_token),
    question_repo: QuestionRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends(),
) -> QuestionSchema:
    username: str = user_service.decode_jwt(access_token=access_token)
    user: User | None = user_repo.get_user(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    question: Question = Question.create(request=request, author_id=user.id)
    question: Question = question_repo.create_question(question=question)

    return QuestionSchema.from_orm(question)

@router.patch("/{question_id}", status_code=200)
def update_question_handler(
    question_id: int,
    request: CreateQuestionRequest,
    access_token: str = Depends(get_access_token),
    question_repo: QuestionRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends(),
):
    username: str = user_service.decode_jwt(access_token=access_token)
    user: User | None = user_repo.get_user(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    question: Question | None = question_repo.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if question.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_question = question.update(request=request, question=question)
    question: Question = question_repo.update_question(question=update_question)

    return QuestionSchema.from_orm(question)

@router.delete("/{question_id}", status_code=204)
def delete_question_handler(
    question_id: int,
    access_token: str = Depends(get_access_token),
    question_repo: QuestionRepository = Depends(),
    user_repo: UserRepository = Depends(),
    user_service: UserService = Depends(),
):
    username: str = user_service.decode_jwt(access_token=access_token)
    user: User | None = user_repo.get_user(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    question: Question | None = question_repo.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if question.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    question_repo.delete_question(question=question)

