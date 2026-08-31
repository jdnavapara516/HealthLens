# HealthLens AI

HealthLens AI is a full-stack medical document intelligence platform that allows users to upload health documents, chat with an AI assistant about them, and manage their account securely.

It combines:
- Django for the web app, authentication, user profile, dashboard, and document management
- FastAPI for AI processing, chat orchestration, and ingestion workflows
- PostgreSQL with pgvector for document/chunk storage and retrieval
- Docker Compose for local and production-style deployment

## Overview

The project is designed for a healthcare-oriented workflow where a user can:
- create an account and sign in
- upload medical or health-related documents
- process those documents through the AI backend
- ask questions about the uploaded content in a chat interface
- review report history and manage saved data
- reset their account data or change password through Django auth flows

## Architecture

- Django frontend: `django/`
- FastAPI API: `fastapi/`
- PostgreSQL database: configured via Docker Compose
- AI ingestion and retrieval workflow: implemented in the FastAPI service
- User auth and profile management: handled by Django’s built-in auth system and custom account views

## Tech Stack

### Django app
- Python 3.12
- Django 6.1
- PostgreSQL
- Django templates with custom CSS/JS
- Authentication, profile management, password reset, and dashboard flows

### FastAPI app
- FastAPI
- SQLAlchemy
- pgvector
- LangChain / LangGraph
- Groq / Hugging Face model integrations
- PDF and document processing utilities

## Repository Structure

```bash
.
├── docker-compose.yml
├── docker-compose.prod.yml
├── Dockerfile.django
├── Dockerfile.fastapi
├── .env.example
├── README.md
├── django/
│   ├── accounts/
│   ├── chat/
│   ├── config/
│   ├── media/
│   ├── reports/
│   ├── static/
│   ├── templates/
│   ├── manage.py
│   ├── requirements.txt
│   └── venv/
├── fastapi/
│   ├── alembic/
│   ├── app/
│   ├── tests/
│   ├── alembic.ini
│   └── requirements.txt
└── .gitignore
```

## Features

- User signup / login / logout
- Password change and password reset via Django auth views
- User profile page with account management
- Document upload and storage
- AI-powered chat on uploaded reports
- Report listing and detail views
- Data reset for user-specific saved content
- Dockerized setup for local development and deployment

## Environment Setup

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Then update values such as:
- `SECRET_KEY`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `FASTAPI_URL`
- `HF_TOKEN`
- `GROQ_API_KEY`
- `GROQ_MODEL`
- `EMBEDDING_MODEL`

## Running with Docker Compose

Start the full stack:

```bash
docker compose up --build
```

This starts:
- PostgreSQL on `localhost:5432`
- FastAPI on `localhost:8000`
- Django app on `localhost:8001`

To stop it:

```bash
docker compose down
```

## Running Locally (without Docker)

### 1) Create and activate a virtual environment

```bash
cd django
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2) Start PostgreSQL
Ensure PostgreSQL is running locally or use the Docker database service.

### 3) Apply migrations

```bash
python manage.py migrate
```

### 4) Start the Django app

```bash
python manage.py runserver 8001
```

### 5) Start the FastAPI service

In a separate terminal:

```bash
cd fastapi
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Default URLs

Once the Django app is running:
- Landing page: `http://localhost:8001/`
- Login: `http://localhost:8001/login/`
- Signup: `http://localhost:8001/signup/`
- Profile: `http://localhost:8001/profile/`
- Password change: `http://localhost:8001/password/change/`

FastAPI endpoints are served on:
- `http://localhost:8000`

## Production Deployment

A production-style Compose configuration is available in:

- `docker-compose.prod.yml`

This is intended for deployment environments where you provide environment variables securely and run the containers with production settings.

## Notes

- Django handles the website experience and user account flows.
- FastAPI handles the AI ingestion, chat, and document-processing logic.
- The database is configured for vector support, which is required for retrieval-based chat features.
- Static media files are stored under the Django `media/` directory.

## License

This project is intended for internal/demo usage unless a project-specific license is added later.
