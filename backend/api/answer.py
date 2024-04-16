from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from db.repository import AnswerRepository, QuestionRepository
from db.orm import Answer, Question
from schema.question.request import CreateAnswerRequest
from schema.question.response import AnswerSchema


router = APIRouter(prefix="/answer")

@router.get("/{answer_id}", status_code=200)

@router.post("/create/{question_id}", status_code=201)
def create_answer_handler(
    question_id: int,
    answer: CreateAnswerRequest,
    answer_repo: AnswerRepository = Depends(),
    question_repo: QuestionRepository = Depends(),
) -> AnswerSchema:
    question: Question | None = question_repo.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    answer: Answer = Answer.create(question_id=question.id, request=answer)
    answer: Answer = answer_repo.create_answer(answer=answer)
    return AnswerSchema.from_orm(answer)

@router.patch("/update/{answer_id}", status_code=200)
def update_answer_handler(
    answer_id: int,
    request: CreateAnswerRequest,
    answer_repo: AnswerRepository = Depends()
) -> AnswerSchema:
    answer: Answer | None = answer_repo.get_answer_by_answer_id(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    update_answer: Answer = answer.update(answer=answer, request=request)

    answer: Answer = answer_repo.update_answer(answer=update_answer)
    return AnswerSchema.from_orm(answer)

@router.delete("/delete/{answer_id}", status_code=204)
def delete_answer_handler(
    answer_id: int,
    answer_repo: AnswerRepository = Depends(),
):
    answer: Answer | None = answer_repo.get_answer_by_answer_id(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    answer_repo.delete_answer(answer=answer)
    
