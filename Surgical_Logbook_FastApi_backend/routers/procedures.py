from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from models import Procedure, ProcedureCreate, ProcedureRead, User
from database import get_session
from schema import ApiResponse
from security import get_current_admin

router = APIRouter(prefix="/procedures", tags=["Procedures"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=ApiResponse[list[ProcedureRead]])
async def read_procedures(session: SessionDep):
    procedures = session.exec(select(Procedure).order_by(Procedure.specialty, Procedure.name)).all()
    return ApiResponse(data=procedures)

@router.get("/{procedure_id}", response_model=ApiResponse[ProcedureRead])
async def read_procedure(procedure_id: int, session: SessionDep):
    procedure = session.get(Procedure, procedure_id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure Not Found")
    return ApiResponse(data=procedure)

@router.post("/", status_code=201, response_model=ApiResponse[ProcedureRead])
async def create_procedure(procedure: ProcedureCreate, session: SessionDep, current_user:User = Depends(get_current_admin)):
    # normalize first
    new_procedure = Procedure.model_validate(procedure)
    # unique
    exists = session.exec(select(Procedure).where(Procedure.name == new_procedure.name)).first()

    if exists:
        raise HTTPException(status_code=400, detail="Procedure already exists!")
    
    session.add(new_procedure)
    session.commit()
    session.refresh(new_procedure)
    return ApiResponse(data=new_procedure)

@router.put("/{procedure_id}", response_model=ApiResponse[ProcedureRead])
async def update_procedure(procedure_id: int, updated: ProcedureCreate, session: SessionDep, current_user:User = Depends(get_current_admin)):

    db_procedure = session.get(Procedure, procedure_id)

    if not db_procedure:
        raise HTTPException(status_code=404, detail="Procedure Not Found!")


    # uniqueness check
    exists = session.exec(select(Procedure).where(Procedure.name == updated.name).where(Procedure.id != procedure_id)).first()

    if exists:
        raise HTTPException(status_code=400, detail="Procedure name already exists")

    # update do not add new row
    db_procedure.name = updated.name
    db_procedure.specialty = updated.specialty
    
    session.commit()
    session.refresh(db_procedure)

    return ApiResponse(data=db_procedure)

@router.delete("/{procedure_id}", status_code=204)
async def delete_procedure(procedure_id: int, session: SessionDep, current_user:User = Depends(get_current_admin)):
    procedure = session.get(Procedure, procedure_id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure Not Found")
    
    try:
        session.delete(procedure)
        session.commit()
    except IntegrityError:
        session.rollback
        raise HTTPException(status_code=400, detail="Procedure cannot be deleted because it is referenced by one or more surgical logs.")