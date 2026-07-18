# Surgical Logbook API

## Overview

Surgical Logbook API is a backend application built with FastAPI and PostgreSQL.

The project is my modern interpretation of what a surgical training logbook should look like. It allows surgeons to securely record operative experience across procedures, specialties, hospitals, and levels of involvement.

The application also includes role-based admin access for managing data and viewing platform-wide analytics.

---

## Features

- JWT-based authentication
- Role-based authorization (Admin vs Regular User)
- CRUD operations for users, logs, procedures, and hospitals
- Filtering and pagination for logs retrieval
- User analytics dashboard
- Admin analytics dashboard with:
  - total users
  - active users
  - total logs
  - hospital/specialty activity distribution


## Tech Stack

- FastAPI
- Pydantic
- SQLModel
- PostgreSQL
- JWT Authentication


## Setup

Install dependencies:

pip install -r requirements.txt

Run the server:
uvicorn main:app --reload

## Enviromental variables

create .env file with :
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=

## API Demo

YouTube demonstration : https://youtu.be/Hq-JGEAj6M4?si=unbT0i7z6KobyIOP

## Future Improvements

This project represents Version 1 of a larger platform.

Planned future improvements include:

React frontend integration
Deployment to cloud infrastructure
CSV data migration support
LLM-powered analytics and training insights
Enhanced surgical training performance tracking