from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from sqlmodel import Session, select

from database import get_session
from models import User, UserLogin
from security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/authentication", tags=["Authentication"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.post('/login')
def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    # swagger needs username instead of registration & password
    user_data = session.exec(select(User).where(User.registration == form_data.username)).first()
    if not user_data:
        raise HTTPException(status_code=403, detail="Invalid Credentials!")
    
    if not verify_password(form_data.password, user_data.hash):
        raise HTTPException(status_code=403, detail="Invalid Credentials!")
    
# CREATE TOKEN
    token = create_access_token(data= {"sub":str(user_data.id),"role": user_data.role.value})
    return {"access_token" : token, "token_type": "bearer"}
