from sqlmodel import Session, select
from models import Procedure

def seed_procedures(session:Session):
    procedures = [

    # General Surgery
    {"name": "Appendicectomy", "specialty": "General Surgery"},
    {"name": "Incision and Drainage Abscess", "specialty": "General Surgery"},
    {"name": "Inguinal Hernia Repair", "specialty": "General Surgery"},
    {"name": "Excision of Lump / Cyst", "specialty": "General Surgery"},
    {"name": "Cholecystectomy", "specialty": "General Surgery"},
    {"name": "Para-Umbilical Hernia Repair", "specialty": "General Surgery"},
    {"name": "Incisional Hernia Repair", "specialty": "General Surgery"},
    {"name": "Laparotomy", "specialty": "General Surgery"},


    # Breast Surgery
    {"name": "Breast Lumpectomy", "specialty": "Breast Surgery"},
    {"name": "Wide Local Excision", "specialty": "Breast Surgery"},
    {"name": "Sentinel Lymph Node Biopsy", "specialty": "Breast Surgery"},
    {"name": "Axillary Lymph Node Clearance", "specialty": "Breast Surgery"},
    {"name": "Mastectomy", "specialty": "Breast Surgery"},
    {"name": "Reduction Mammoplasty", "specialty": "Breast Surgery"},


    # Upper GI Surgery
    {"name": "Oesophagectomy", "specialty": "Upper GI Surgery"},
    {"name": "Gastrectomy", "specialty": "Upper GI Surgery"},
    {"name": "Gastrojejunostomy", "specialty": "Upper GI Surgery"},
    {"name": "Hiatus Hernia Repair", "specialty": "Upper GI Surgery"},
    {"name": "Sleeve Gastrectomy", "specialty": "Upper GI Surgery"},
    {"name": "Laparoscopic Nissen Fundoplication", "specialty": "Upper GI Surgery"},


    # Colorectal Surgery
    {"name": "Right Hemicolectomy", "specialty": "Colorectal Surgery"},
    {"name": "Left Hemicolectomy", "specialty": "Colorectal Surgery"},
    {"name": "Low Anterior Resection", "specialty": "Colorectal Surgery"},
    {"name": "Abdominoperineal Resection", "specialty": "Colorectal Surgery"},
    {"name": "Total Colectomy", "specialty": "Colorectal Surgery"},
    {"name": "Colostomy Formation", "specialty": "Colorectal Surgery"},
    {"name": "Ileostomy Formation", "specialty": "Colorectal Surgery"},
    {"name": "Haemorrhoidectomy", "specialty": "Colorectal Surgery"},


    # Vascular Surgery
    {"name": "Carotid Endarterectomy", "specialty": "Vascular Surgery"},
    {"name": "Femoral Endarterectomy", "specialty": "Vascular Surgery"},
    {"name": "Femoral Popliteal Bypass", "specialty": "Vascular Surgery"},
    {"name": "Abdominal Aortic Aneurysm Repair", "specialty": "Vascular Surgery"},
    {"name": "Endovascular Aneurysm Repair", "specialty": "Vascular Surgery"},
    {"name": "Varicose Vein Surgery", "specialty": "Vascular Surgery"},
    {"name": "Arteriovenous Fistula Formation", "specialty": "Vascular Surgery"},


    # Urology
    {"name": "Transurethral Resection of Prostate", "specialty": "Urology"},
    {"name": "Transurethral Resection of Bladder Tumour", "specialty": "Urology"},
    {"name": "Radical Prostatectomy", "specialty": "Urology"},
    {"name": "Nephrectomy", "specialty": "Urology"},
    {"name": "Partial Nephrectomy", "specialty": "Urology"},
    {"name": "Ureteroscopy", "specialty": "Urology"},
    {"name": "Cystoscopy", "specialty": "Urology"},
    {"name": "Percutaneous Nephrolithotomy", "specialty": "Urology"},


    # Orthopaedics
    {"name": "Total Hip Replacement", "specialty": "Orthopaedics"},
    {"name": "Total Knee Replacement", "specialty": "Orthopaedics"},
    {"name": "Anterior Cruciate Ligament Reconstruction", "specialty": "Orthopaedics"},
    {"name": "Shoulder Arthroscopy", "specialty": "Orthopaedics"},
    {"name": "Carpal Tunnel Release", "specialty": "Orthopaedics"},
    {"name": "Open Reduction Internal Fixation", "specialty": "Orthopaedics"},
    {"name": "Hip Fracture Fixation", "specialty": "Orthopaedics"},


    # ENT
    {"name": "Tonsillectomy", "specialty": "ENT"},
    {"name": "Adenoidectomy", "specialty": "ENT"},
    {"name": "Septoplasty", "specialty": "ENT"},
    {"name": "Functional Endoscopic Sinus Surgery", "specialty": "ENT"},
    {"name": "Grommet Insertion", "specialty": "ENT"},
    {"name": "Mastoidectomy", "specialty": "ENT"},
    {"name": "Parotidectomy", "specialty": "ENT"},
    {"name": "Neck Dissection", "specialty": "ENT"},
]

    for item in procedures:
        existing = session.exec(select(Procedure).where(Procedure.name == item ["name"])).first()

        if not existing:
            procedure = Procedure(**item)
            session.add(procedure)

    session.commit()
    print("Procedures seeded successfully")