from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.connection import get_db
from db.repository import QuestionRepository
from db.orm import Question
from schema.question.response import QuestionListSchema, QuestionSchema
from schema.question.request import CreateQuestionRequest


router = APIRouter(prefix="/question")

@router.get("/list", status_code=200)
def get_questions_handler(
    order: str | None = None,
    question_repo: QuestionRepository = Depends(),
):
    question_list: List[QuestionListSchema] = question_repo.get_question_list()

    if order and order == "desc":
        return question_list[::-1]
    return question_list

@router.get("/{question_id}", status_code=200)
def get_question_handler(
    question_id: int,
    question_repo: QuestionRepository = Depends(),
) -> QuestionSchema:
    question: Question = question_repo.get_question_by_id(question_id)

    if question:
        return QuestionSchema.from_orm(question)
    raise HTTPException(status_code=404, detail="Question not found")

@router.post("", status_code=201)
def create_question_handler(
    request: CreateQuestionRequest,
    question_repo: QuestionRepository = Depends(),
) -> QuestionSchema:
    question: Question = Question.create(request=request)
    question: Question = question_repo.create_question(question=question)

    return QuestionSchema.from_orm(question)

@router.patch("/{question_id}", status_code=200)
def update_question_handler(
    question_id: int,
    request: CreateQuestionRequest,
    question_repo: QuestionRepository = Depends(),
):
    question: Question | None = question_repo.get_question_by_id(question_id)

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    update_question = question.update(request=request, question=question)
    question: Question = question_repo.update_question(question=update_question)

    return QuestionSchema.from_orm(question)

@router.delete("/{question_id}", status_code=204)
def delete_question_handler(
    question_id: int,
    question_repo: QuestionRepository = Depends(),
):
    question: Question | None = question_repo.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question_repo.delete_question(question=question)

