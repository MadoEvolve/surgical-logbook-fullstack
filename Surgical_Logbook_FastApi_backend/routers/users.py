from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from database import get_session

from models import User, UserRead, UserCreate, UserUpdate, UserRole, Log
from security import hash_password, get_current_user, get_current_admin

from schema import ApiResponse, UserSummary


router = APIRouter(prefix="/users", tags=["users"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=ApiResponse[list[UserRead]])
async def read_users(session: SessionDep, current_user:User = Depends(get_current_admin)):
    users = session.exec(select(User)).all()
    return ApiResponse(data=users)

@router.get("/me", response_model=ApiResponse[UserRead])
async def read_me(current_user: User = Depends(get_current_user)):
    return ApiResponse(data=current_user)

@router.get("/summary", response_model=ApiResponse[list[UserSummary]])
async def read_summary(session: SessionDep, current_user:User= Depends(get_current_admin)):
    query = select(User.id, User.username, User.registration, User.email, User.role,
            func.count(Log.id).label("total_logs")).outerjoin(
            Log, Log.user_id == User.id).group_by(User.id)

    summary = [UserSummary(
        id=row.id, username=row.username, registration=row.registration, email=row.email,
        role=row.role, total_logs=row.total_logs) for row in  session.exec(query)
        ]
    return ApiResponse(data=summary)

@router.get("/{user_id}", response_model=ApiResponse[UserRead])
async def read_user(session: SessionDep, user_id:int, current_user:User = Depends(get_current_user)):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.role != UserRole.admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorised")
    return ApiResponse(data=user)

@router.post("/", status_code=201, response_model=ApiResponse[UserRead])
async def create_user(session: SessionDep, user:UserCreate):
    # unique registration
    exists = session.exec(select(User).where(User.registration == user.registration)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Registration already exists!")
    
    hash_pw = hash_password(user.password)
    new_user = User(username= user.username, registration=user.registration, email=user.email, hash=hash_pw)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return ApiResponse(data=new_user)

@router.put("/{user_id}", response_model=ApiResponse[UserRead])
async def update_user(session: SessionDep, user_id:int, updated: UserUpdate, current_user:User = Depends(get_current_user)):
    db_user = session.get(User,user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found!")
    
    # only admin and current user can update the account
    if current_user.role != UserRole.admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not Authorised")
    
    # unique registration
    exists = session.exec(select(User).where(User.registration == updated.registration).where(User.id != user_id)).first()
    if exists:
        raise HTTPException(status_code=400, detail="User already exists!")
    
    if updated.password:
        db_user.hash = hash_password(updated.password)
    # updated version
    db_user.username = updated.username
    db_user.registration = updated.registration
    db_user.email = updated.email
    
    
    session.commit()
    session.refresh(db_user)
    return ApiResponse(data=db_user)

@router.delete("/{user_id}", status_code=204)
async def delete_user(session: SessionDep,user_id: int,current_user: User = Depends(get_current_user)):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    # only admin and current user can delete the account
    if current_user.role != UserRole.admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorised")
    if user.id == current_user.id:
        raise HTTPException(status_code=400,detail="You cannot delete your own account.")

    try:
        session.delete(user)
        session.commit()
    except IntegrityError:
        session.rollback
        raise HTTPException(status_code=400, detail="User cannot be deleted because it is referenced by one or more surgical logs.")