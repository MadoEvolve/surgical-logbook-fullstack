from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated, Optional
from sqlalchemy import func
from sqlmodel import Session, select
from datetime import date

from models import Log, LogCreate, LogRead, LogDetailRead, User, Procedure, Hospital
from database import get_session
from schema import ApiResponse, PaginatedLogs
from security import get_current_user, get_current_admin

router = APIRouter(prefix="/logs", tags=["Logs"])

SessionDep = Annotated[Session, Depends(get_session)]


# helper function
def build_log_details(logs):
    return [
        LogDetailRead(
            id=log.id,
            user_id=log.user_id,
            username=log.user.username,
            procedure_id=log.procedure_id,
            procedure_name=log.procedure.name,
            hospital_id=log.hospital_id,
            hospital_name=log.hospital.name,
            role=log.role,
            notes=log.notes,
            procedure_date=log.procedure_date,
            log_clock=log.log_clock,
        )
        for log in logs
    ]
# get logs per user with pagination & has to be top me not int{log_id}
@router.get("/me", response_model=ApiResponse[PaginatedLogs])
async def read_my_logs(session: SessionDep,current_user: User = Depends(get_current_user),
    procedure_id: Optional[int] = None,hospital_id: Optional[int] = None,limit: int = 10,offset: int = 0):
    
    query = select(Log).where(Log.user_id == current_user.id)
    
    if procedure_id:
        query = query.where(Log.procedure_id == procedure_id)

    if hospital_id:
        query = query.where(Log.hospital_id == hospital_id)
    
    count_query = query
    query = query.offset(offset).limit(limit)
    logs = session.exec(query).all()
    total = session.exec(select(func.count()).select_from(count_query.subquery())).one()

    # building the LogDetailRead for Frontend
    result = build_log_details(logs)

    return ApiResponse(data=PaginatedLogs(result=result, total=total))

# amended to search logs rather than read all logs
@router.get("/",response_model=ApiResponse[PaginatedLogs])
async def search_logs(session: SessionDep, current_user:User = Depends(get_current_admin),
    specialty: Optional[str] = None, location: Optional[str] = None,
    procedure_id: Optional [int]=None, hospital_id: Optional [int]=None,
    user_id: Optional[int]=None, start_date: Optional[date]=None,
    end_date:Optional[date]=None,limit: int=100, offset: int=0):
    
    query = select(Log).order_by(Log.log_clock.desc())

    if specialty:
        query = (query.join(Procedure).where(Procedure.specialty == specialty))

    if location:
        query = (query.join(Hospital).where(Hospital.location == location))
    if user_id:
        query =  query.where(Log.user_id == user_id)
    if procedure_id:
        query = query.where(Log.procedure_id == procedure_id)
    if hospital_id:
        query = query.where(Log.hospital_id == hospital_id)
    if start_date:
        query = query.where(Log.procedure_date >= start_date)

    if end_date:
        query = query.where(Log.procedure_date <= end_date)
    
    # Save the filtered query before applying pagination.
    # We'll use it to calculate the total number of matching rows.
    count_query = query
    # execute the paginated query with the given parameters
    query = query.offset(offset).limit(limit)
    logs = session.exec(query).all()

    # count before pagination
    total = session.exec(select(func.count()).select_from(count_query.subquery())).one()
    # formulate response
    result = build_log_details(logs)
    
    return ApiResponse(data=PaginatedLogs(result=result, total=total))

@router.get("/{log_id}",response_model=ApiResponse[LogRead])
async def read_log(session: SessionDep,log_id:int):
    log = session.get(Log,log_id)
    if not log:
        raise HTTPException(status_code=404,detail="log not Found")
    return ApiResponse(data=log)

@router.post("/",status_code=201,response_model=ApiResponse[LogRead])
async def create_log(session: SessionDep,log: LogCreate,current_user: User = Depends(get_current_user)):
    # validate foreign keys

    procedure = session.get(Procedure,log.procedure_id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not Found")
    hospital = session.get(Hospital,log.hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not Found")
    
    new_log= Log(**log.model_dump(), user_id=current_user.id)
    session.add(new_log)
    session.commit()
    session.refresh(new_log)

    return ApiResponse(data=new_log)

@router.put("/{log_id}", response_model=ApiResponse[LogDetailRead])
async def update_log(session: SessionDep, updated: LogCreate, log_id:int, current_user:User = Depends(get_current_user)):
    db_log = session.get(Log, log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    # verifying only the user can edit their log
    if db_log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorised Access")
    # Verifying foreign keys
    procedure = session.get(Procedure,updated.procedure_id)
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not Found")
    hospital = session.get(Hospital,updated.hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not Found")
    

    db_log.procedure_id = updated.procedure_id
    db_log.hospital_id = updated.hospital_id
    db_log.role = updated.role
    db_log.notes = updated.notes
    db_log.procedure_date = updated.procedure_date
    session.add(db_log)
    session.commit()
    session.refresh(db_log)


    return ApiResponse(data=build_log_details([db_log])[0])

@router.delete("/{log_id}", status_code=204)
async def delete_log(session : SessionDep, log_id:int, current_user: User = Depends(get_current_user)):
    db_log = session.get(Log, log_id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    # verifying only the user can edit their log
    if db_log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorised Access")
    
    session.delete(db_log)
    session.commit()

