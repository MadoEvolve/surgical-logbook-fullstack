from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated, Optional
from sqlmodel import Session, select
from sqlalchemy import func, label

from models import Log, User, Procedure, Hospital, UserStats, HospitalSpecialtyStats, AdminStats
from database import get_session
from schema import ApiResponse 
from security import get_current_user, get_current_admin

router = APIRouter(prefix="/stats", tags=["stats"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/me", response_model= ApiResponse[UserStats])
async def summarise_logs(session: SessionDep, current_user: User = Depends(get_current_user)):
    # Q1 total logs count
    user_total_logs = session.exec(select(func.count(Log.id)).where(Log.user_id == current_user.id)).one()

    # Q2 role_breakdown
    # query returns a list of tuples
    role_stats = session.exec(select(Log.role, func.count(Log.id).label("count")).where(Log.user_id == current_user.id).group_by(Log.role)).all()
    # transform into dict fitting the schema
    user_role_breakdown = {role.value: count for role, count in role_stats}

    # Q3 specialty_breakdown
    specialty_stats= session.exec(select(Procedure.specialty, func.count(Log.id).label("count"))
                            .join (Log, Procedure.id == Log.procedure_id)
                            .where(Log.user_id == current_user.id).group_by (Procedure.specialty)).all() 
    user_specialty_stats = {specialty : count for specialty,count in specialty_stats}
    # fitting into ApiResponse
    user_stats = UserStats(total_logs = user_total_logs, role_breakdown = user_role_breakdown, specialty_breakdown = user_specialty_stats)
    
    return ApiResponse(data=user_stats)

@router.get("/admin", response_model=ApiResponse[AdminStats])
async def admin_view(session: SessionDep, current_user: User = Depends(get_current_admin)):
    # total users, logs
    total_users = session.exec(select(func.count(User.id))).one()
    active_users, total_logs = session.exec(select(func.count(func.distinct(Log.user_id)),func.count(Log.id))).one()

    # HospitalSpecialtyStats
    hss_tuples = session.exec(select(Hospital.name, Procedure.specialty, func.count(Log.id))
                         .join(Procedure, Procedure.id == Log.procedure_id).join(Hospital, Hospital.id == Log.hospital_id)
                         .group_by(Hospital.name, Procedure.specialty)
                         .order_by(Hospital.name, Procedure.specialty)).all()
    hospital_specialty_stats = [HospitalSpecialtyStats(hospital=hospital,specialty=specialty,logs=logs)for hospital, specialty, logs in hss_tuples]

    global_stats = AdminStats(total_users=total_users, active_users=active_users, total_logs=total_logs,hospital_specialty_stats=hospital_specialty_stats)
    return ApiResponse(data= global_stats)