import random
from datetime import date
from faker import Faker

from sqlmodel import Session, select
from models import Log, RoleEnum, User, UserRole,Procedure, Hospital

fake = Faker("en_GB")

def seed_logs(session: Session):
    # get all fake users , hospitals, procedures list of objects
    
    users = session.exec(
    select(User).where(User.role == UserRole.user)).all()
    procedures = session.exec(select(Procedure)).all()
    hospitals = session.exec(select(Hospital)).all()

    # 30-100 logs per user
    for user in users:
        n_logs = random.randint(30, 100)
        for _ in range(n_logs):
            procedure = random.choice(procedures)
            hospital = random.choice(hospitals)
            role = random.choice(list(RoleEnum))
            procedure_date = fake.date_between(start_date="-2y",end_date="today",)
            notes = random.choice([None,None,None,fake.sentence()])

            # create the log
            fake_log= Log(user_id=user.id,
                procedure_id=procedure.id,
                hospital_id=hospital.id,
                role=role,
                procedure_date=procedure_date,
                notes=notes,)
            session.add(fake_log)

    session.commit()