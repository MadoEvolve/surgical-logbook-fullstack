# Surgical Logbook

A full-stack web application for recording and managing surgical training experience.

The project is my interpretation of what a modern surgical logbook should look like. It enables healthcare professionals to securely record procedures, track operative experience across multiple specialties and hospitals, and analyse training activity through interactive dashboards.

The application is built with a FastAPI backend, a React frontend, and PostgreSQL, following a modern API-first architecture.

---

## Features

### Authentication & Security

* JWT-based authentication
* Secure password hashing
* Role-based authorization (Admin and User roles)
* Protected API endpoints

### Surgical Log Management

* Create, edit and delete surgical log entries
* Record:

  * Procedure
  * Hospital
  * Date
  * Level of involvement
  * Personal notes
* Search and filter logs by:

  * User
  * Specialty
  * Procedure
  * Location
  * Hospital
  * Date range
* Pagination for efficient browsing

### Administration

Administrators can:

* Manage users
* Manage hospitals
* Manage procedures
* View all surgical logs
* Access platform-wide statistics

### Analytics

User dashboard includes:

* Total procedures performed
* Procedure role breakdown
* Specialty activity breakdown

Administrator dashboard includes:

* Total registered users
* Active users
* Total logged procedures
* Hospital and specialty activity statistics

### Realistic Demo Data

The project includes database seed scripts that generate:

* UK hospitals
* Surgical procedures across multiple specialties
* Demo users
* Hundreds of realistic surgical log entries using Faker

---

## Tech Stack

### Backend

* FastAPI
* SQLModel
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* PyJWT
* Passlib
* Faker
* Pytest

### Frontend

* React
* React Router
* Vite
* JavaScript
* CSS

---

## Project Structure

surgical-logbook-fullstack/
│
├── Surgical_Logbook_FastApi_backend/
│   ├── alembic/
│   ├── routers/
│   ├── scripts/
│   ├── tests/
│   └── ...
│
├── surgical-logbook-frontend/
│   ├── src/
│   ├── public/
│   └── ...
│
└── README.md

---

## Getting Started

### 1. Clone the repository


git clone https://github.com/MadoEvolve/surgical-logbook-fullstack.git
cd surgical-logbook-fullstack


### 2. Backend

cd Surgical_Logbook_FastApi_backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

Create a `.env` file containing:

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

Run database migrations:

alembic upgrade head


(Optional) Populate the database:

python -m scripts.seed

Start the API:

uvicorn main:app --reload

---

### 3. Frontend

cd surgical-logbook-frontend

npm install
npm run dev

---

## Testing

Backend tests are written using Pytest.

Run the test suite with:

pytest


---

## Current Status

Completed:

* FastAPI REST API
* React frontend
* PostgreSQL database
* Alembic migrations
* JWT authentication
* Role-based authorization
* Pagination and filtering
* Search by specialty and location
* Seed scripts with realistic demo data
* Automated backend tests

---

## Roadmap

Planned improvements include:

* Docker containerization
* Cloud deployment
* CI/CD pipeline
* CSV import/export
* Enhanced analytics dashboard
* AI-powered training insights
* Natural language search
* Performance recommendations based on operative history

---

## Demo

A new walkthrough video covering both the backend API and the React frontend will be published after deployment.

---

## About This Project

This project began as a learning exercise while studying modern Python web development and has gradually evolved into a complete full-stack portfolio application.

Rather than focusing only on implementing features, the project has also explored practical software engineering concepts including database migrations, testing, authentication, project structure, realistic data seeding, and full-stack integration.
