from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from models import Hospital, HospitalRead, HospitalCreate, User
from database import get_session
from schema import ApiResponse 
from security import get_current_admin

router = APIRouter(prefix="/hospitals", tags=["hospitals"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=ApiResponse[list[HospitalRead]])
async def read_hospitals(session: SessionDep):
    hospitals = session.exec(select(Hospital)).all()
    return ApiResponse(data=hospitals)

@router.get("/{hospital_id}", response_model=ApiResponse[HospitalRead])
async def read_hospital(session: SessionDep, hospital_id: int):
    hospital = session.get(Hospital, hospital_id)

    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return ApiResponse(data=hospital)

@router.post("/", status_code=201, response_model=ApiResponse[HospitalRead])
async def create_hospital(session:SessionDep, hospital: HospitalCreate, current_user:User = Depends(get_current_admin)):
    # normalise input
    new_hospital = Hospital.model_validate(hospital)
    # unique
    exists = session.exec(select(Hospital).where(Hospital.name == new_hospital.name)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Hospital already exists!")
    
    
    session.add(new_hospital)
    session.commit()
    session.refresh(new_hospital)
    return ApiResponse(data=new_hospital)

@router.put("/{hospital_id}", response_model=ApiResponse[HospitalRead])
async def update_hospital(session: SessionDep, hospital_id: int, updated: HospitalCreate,current_user:User = Depends(get_current_admin)):
    db_hospital = session.get(Hospital, hospital_id)
    if not db_hospital:
        raise HTTPException(status_code=404, detail="Hospital Not Found!")
    
    # unique update
    exists = session.exec(select(Hospital).where(Hospital.name == updated.name).where(Hospital.id != hospital_id)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Hospital already exists!")
    
    db_hospital.name = updated.name
    db_hospital.location = updated.location
    
    session.commit()
    session.refresh(db_hospital)
    return ApiResponse(data=db_hospital)

@router.delete("/{hospital_id}", status_code=204)
async def delete_hospital(hospital_id: int,session: SessionDep,current_user: User = Depends(get_current_admin)):
    hospital = session.get(Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    try:
        session.delete(hospital)
        session.commit()
    # admin can't delete relational db
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400,
            detail="Hospital cannot be deleted because it is referenced by one or more surgical logs.")
    
