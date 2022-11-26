from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import model, schema,crud
from typing import List
from  ..oauth2 import get_current_user
from ..database import get_db


router = APIRouter(prefix="/Polls", tags=["Polls"])


def get_question_obj(db, qid):
	obj = crud.get_question(db=db, qid=qid)
	if obj is None:
		raise HTTPException(status_code=404, detail="Question not found")
	return obj


# @router.post("/questions/")
@router.post("/questions/", response_model=schema.QuestionInfo)
def create_question(question: schema.QuestionCreate, db: Session = Depends(get_db),user: int = Depends(get_current_user)):
	return crud.create_question(db=db, question=question,user=user)
    # return {
    #     'qus': question.question_text,
    #     'options': question.choice_text
    # }


@router.get("/questions/", response_model=List[schema.Question])
def get_questions(db: Session = Depends(get_db)):

	return crud.get_all_questions(db=db)

@router.get("/questions/{qid}", response_model=schema.QuestionInfo)
def get_question(qid: int, db: Session = Depends(get_db)):
	return get_question_obj(db=db, qid=qid)
	
@router.put("/questions/{qid}", response_model=schema.QuestionInfo)
def edit_question(qid: int, question: schema.QuestionCreate, db: Session = Depends(get_db)):
	get_question_obj(db=db, qid=qid)
	obj = crud.edit_question(db=db, qid=qid, question=question)
	return obj

@router.delete("/questions/{qid}")
def delete_question(qid: int, db: Session = Depends(get_db)):
	get_question_obj(db=db, qid=qid)
	crud.delete_question(db=db, qid=qid)
	return {"detail": "Question deleted", "status_code": 204}


# Choice

@router.post("/questions/{qid}/choice", response_model=schema.ChoiceList)
def create_choice(qid: int, choice: schema.ChoiceCreate, db: Session = Depends(get_db)):
	get_question_obj(db=db, qid=qid)
	return crud.create_choice(db=db, qid=qid, choice=choice)

@router.put("/choices/{choice_id}/vote", response_model=schema.ChoiceList)
def update_vote(choice_id: int, db: Session = Depends(get_db)):
	return crud.update_vote(choice_id=choice_id, db=db)