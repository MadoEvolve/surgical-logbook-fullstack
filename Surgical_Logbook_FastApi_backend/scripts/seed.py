from sqlmodel import Session
from database import engine

from scripts.seed_hospitals import seed_hospitals
from scripts.seed_procedures import seed_procedures
from scripts.seed_admin import seed_admin
from scripts.seed_users import seed_users
from scripts.seed_logs import seed_logs


def main():
    with Session(engine) as session:
        seed_hospitals(session)
        seed_procedures(session)
        seed_admin(session)
        seed_users(session)
        seed_logs(session)


if __name__ == "__main__":
    main()