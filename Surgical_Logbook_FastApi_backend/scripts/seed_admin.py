from sqlmodel import Session, select
from models import UserRole, User
from security import hash_password

def seed_admin(session: Session):

    admins = [
        {
            "username": "Mado",
            "registration": "12345",
            "email": "mado@example.com",
            "role": UserRole.admin,
            "password": "Mia",
        }
    ]

    for item in admins:

        existing = session.exec(
            select(User).where(User.registration == item["registration"])).first()

        if not existing:
            admin= User(
                username=item["username"],
                registration=item["registration"],
                email=item["email"],
                role=item["role"],
                hash=hash_password(item["password"]),
            )

            session.add(admin)

    session.commit()

    print("Admin seeded successfully")