from enum import Enum
from typing import Optional, List
from datetime import date, datetime

from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func


# PROCEDURE

class ProcedureBase(SQLModel):
    name: str = Field(index=True, sa_column_kwargs={"unique": True})
    specialty: str

    @field_validator("name", "specialty")
    @classmethod
    def normalize_text(cls, v: str) -> str:
        return v.strip().title()


class Procedure(ProcedureBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    logs: List["Log"] = Relationship(back_populates="procedure")


class ProcedureCreate(ProcedureBase):
    pass


class ProcedureRead(ProcedureBase):
    id: int


# HOSPITAL

class HospitalBase(SQLModel):
    name: str = Field(index=True, sa_column_kwargs={"unique": True})
    location: str

    @field_validator("name", "location")
    @classmethod
    def normalize_text(cls, v: str) -> str:
        return v.strip().title()


class Hospital(HospitalBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    logs: List["Log"] = Relationship(back_populates="hospital")


class HospitalCreate(HospitalBase):
    pass


class HospitalRead(HospitalBase):
    id: int


# USER


class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    
class UserBase(SQLModel):
    username: str
    registration: str = Field(index=True, sa_column_kwargs={"unique": True})
    email: EmailStr


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hash: str
    role: UserRole = UserRole.user 
    logs: List["Log"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    role: UserRole

class UserLogin(SQLModel):
    registration: str
    password: str
    
class UserUpdate(SQLModel):
    username: str
    registration: str
    email: EmailStr
    password: Optional[str] = None

# LOG

class RoleEnum(str, Enum):
    performed = "performed"
    observed = "observed"
    assistant = "assistant"
    supervised = "supervised"
    training = "training"


class LogBase(SQLModel):
    #user_id: int = Field(foreign_key="user.id", index=True) --> jwt will handle this
    procedure_id: int = Field(foreign_key="procedure.id", index=True)
    hospital_id: int = Field(foreign_key="hospital.id", index=True)

    role: RoleEnum
    notes: Optional[str] = None
    procedure_date: Optional[date] = None


class Log(LogBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)

    log_clock: Optional[datetime] = Field(default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    user: "User" = Relationship(back_populates="logs")
    procedure: "Procedure" = Relationship(back_populates="logs")
    hospital: "Hospital" = Relationship(back_populates="logs")


class LogCreate(LogBase):
    pass


class LogRead(LogBase):
    id: int
    log_clock: datetime

# for react rendering
class LogDetailRead(SQLModel):
    id: int

    user_id : int
    username : str

    procedure_id: int
    procedure_name: str

    hospital_id: int
    hospital_name: str

    role: RoleEnum
    notes: Optional[str] = None
    procedure_date: Optional[date] = None

    log_clock: datetime


# STATS
class UserStats(SQLModel):
    total_logs: int
    role_breakdown: dict[str, int]
    specialty_breakdown: dict[str, int]

class HospitalSpecialtyStats(SQLModel):
    hospital: str
    specialty: str
    logs: int

class AdminStats(SQLModel):
    total_users : int
    active_users : int
    total_logs: int
    hospital_specialty_stats: list[HospitalSpecialtyStats]

    