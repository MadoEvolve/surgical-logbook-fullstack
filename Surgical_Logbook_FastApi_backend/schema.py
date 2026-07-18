from pydantic import BaseModel
from typing import Generic, TypeVar
from sqlmodel import SQLModel
from models import LogDetailRead


# creating a template response for API
T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    data: T

class PaginatedLogs(SQLModel):
    result: list[LogDetailRead]
    total: int

class UserSummary(SQLModel):
    id: int
    username: str
    registration: str
    email: str
    role: str
    total_logs: int