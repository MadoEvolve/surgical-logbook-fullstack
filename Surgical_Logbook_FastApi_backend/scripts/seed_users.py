from faker import Faker

from sqlmodel import Session, select
from models import UserRole, User
from security import hash_password

fake = Faker("en_GB")
USERS = 50

def seed_users(session: Session):
    for i in range(USERS):
        username = fake.name()
        registration = str(100000 + i)
        email = f"user{i}@logbookdemo.com"
        role = UserRole.user
        password_hash = hash_password("Password123")

        existing = session.exec(
            select(User).where(User.registration == registration)).first()

        if not existing:
            user= User(
                username=username,
                registration=registration,
                email=email,
                role=role,
                hash=password_hash,
            )
            session.add(user)

    session.commit()