from sqlmodel import Session, select
from models import Hospital


def seed_hospitals(session: Session):

    hospitals = [
    {
        "name": "Royal London Hospital",
        "location": "London",
    },
    {
        "name": "St Thomas' Hospital",
        "location": "London",
    },
    {
        "name": "Royal Free Hospital",
        "location": "London",
    },
    {
        "name": "King's College Hospital",
        "location": "London",
    },
    {
        "name": "University College Hospital",
        "location": "London",
    },
    {
        "name": "Addenbrooke's Hospital",
        "location": "Cambridge",
    },
    {
        "name": "John Radcliffe Hospital",
        "location": "Oxford",
    },
    {
        "name": "Queen Elizabeth Hospital Birmingham",
        "location": "Birmingham",
    },
    {
        "name": "Manchester Royal Infirmary",
        "location": "Manchester",
    },
    {
        "name": "Salford Royal Hospital",
        "location": "Manchester",
    },
    {
        "name": "Leeds General Infirmary",
        "location": "Leeds",
    },
    {
        "name": "Sheffield Teaching Hospitals",
        "location": "Sheffield",
    },
    {
        "name": "Royal Victoria Infirmary",
        "location": "Newcastle",
    },
    {
        "name": "University Hospital Southampton",
        "location": "Southampton",
    },
    {
        "name": "Bristol Royal Infirmary",
        "location": "Bristol",
    },
    {
        "name": "Royal Devon University Hospital",
        "location": "Exeter",
    },
    {
        "name": "Nottingham University Hospitals",
        "location": "Nottingham",
    },
    {
        "name": "Royal Liverpool University Hospital",
        "location": "Liverpool",
    },
    {
        "name": "Cardiff University Hospital",
        "location": "Cardiff",
    },
    {
        "name": "Queen Elizabeth University Hospital",
        "location": "Glasgow",
    },
]

    for item in hospitals:

        existing = session.exec(select(Hospital).where(Hospital.name == item["name"])).first()

        if not existing:
            hospital = Hospital(**item)
            session.add(hospital)

    session.commit()

    print("Hospitals seeded successfully")