import sys
from pathlib import Path

# python path to find app
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from main import app

import pytest
import uuid

from sqlmodel import Session
from database import get_session
#override depndency in routers with test dependencies
from tests.test_database import test_engine, get_session as test_get_session
from models import User, UserRole, ProcedureCreate, HospitalCreate, LogCreate, RoleEnum
from security import hash_password
from datetime import date


# Fixtures
@pytest.fixture
def client():
    app.dependency_overrides[get_session] = test_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()

# create database session
@pytest.fixture
def session():
    with Session(test_engine) as session:
        yield session

# create test_user
@pytest.fixture
def test_user(session):
    user = User(
        username="test_user",
        registration=f"user_{uuid.uuid4()}",
        email="user@test.com",
        hash=hash_password("test123"),
        role=UserRole.user
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# create another user
@pytest.fixture
def another_user(session):
    user = User(
        username="test_user",
        registration=f"user_{uuid.uuid4()}",
        email="user@test.com",
        hash=hash_password("test123"),
        role=UserRole.user
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# create test_admin
@pytest.fixture
def test_admin(session):
    admin = User(
        username="test_admin",
        registration=f"admin_{uuid.uuid4()}",
        email="admin@test.com",
        hash=hash_password("admin123"),
        role=UserRole.admin
    )

    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin

# auth headers for user
@pytest.fixture
def user_token_headers(client, test_user):

    response = client.post("/authentication/login",data={"username": test_user.registration,"password": "test123"})
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


# auth headers for admin
@pytest.fixture
def admin_token_headers(client, test_admin):

    response = client.post("/authentication/login",data={"username": test_admin.registration,"password": "admin123"})
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}

# Procedure
@pytest.fixture
def new_procedure():
    return ProcedureCreate(name= f"procedure_{uuid.uuid4()}", specialty= "General Surgery")

@pytest.fixture
def updated_procedure():
    return ProcedureCreate(name=f"updated_{uuid.uuid4()}",specialty="General Surgery")

#Hospital
@pytest.fixture
def new_hospital():
    return HospitalCreate(name= f"hospital_{uuid.uuid4()}", location= "London")

@pytest.fixture
def updated_hospital():
    return HospitalCreate(name=f"updated_{uuid.uuid4()}", location= "Manchester")

#Log
@pytest.fixture
def new_log():
    return LogCreate(
        role=RoleEnum.performed,
        notes="Testing...",
        procedure_date=date.today(),
        procedure_id=1,
        hospital_id=1
    )
#my first factory function
@pytest.fixture
def create_log(client,admin_token_headers,user_token_headers,new_procedure,new_hospital,new_log):

    def _create_log():
        # create procedure
        procedure_response = client.post("/procedures/",headers=admin_token_headers,json=new_procedure.model_dump())
        # extract id
        procedure_id = procedure_response.json()["data"]["id"]

        # create hospital
        hospital_response = client.post("/hospitals/",headers=admin_token_headers,json=new_hospital.model_dump())
        # extract id
        hospital_id = hospital_response.json()["data"]["id"]

        # inject ids
        new_log.procedure_id = procedure_id
        new_log.hospital_id = hospital_id

        # create log
        #("mode=json") date format in procedure date
        response = client.post("/logs/",headers=user_token_headers,json=new_log.model_dump(mode="json"))

        return response

    return _create_log

# updated_log
@pytest.fixture
def updated_log():

    return LogCreate(
        procedure_id=1,
        hospital_id=1,
        role=RoleEnum.assistant,
        notes="Updated notes",
        procedure_date=date.today()
    )