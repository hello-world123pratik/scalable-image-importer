# Scalable Django Image Importer

A production-ready, multi-service backend system to import images from public Google Drive folders, store them in S3-compatible object storage, and persist metadata in PostgreSQL.  
The system is designed for scalability, fault tolerance, and large-scale asynchronous processing.

## Architecture

flowchart LR
    UI[React Frontend]
    API[Django API]
    Redis[(Redis)]
    PG[(Postgres)]
    MinIO[(MinIO / S3)]

    Importer[Celery Importer]
    Uploader[Celery Uploader]

    UI --> API
    API --> Redis
    API --> PG

    Redis --> Importer
    Importer --> Uploader
    Uploader --> MinIO
    Uploader --> PG

## Tech Stack

Component            Technology

Frontend             React + Vite

Backend API          Django REST Framework

Async Jobs           Celery

Message Broker       Redis

Database             PostgreSQL

Object Storage       MinIO (S3-compatible)

Containerization     Docker & Docker Compose

## Local Development Setup

1️ Clone Repository

git clone <YOUR_REPO_URL>
cd services/django-api

2️ Environment Variables

cp .env.example .env

3️ Start All Services

docker compose up --build

## Running Services

Service           URL

Django API        http://localhost:8000

MinIO Console     http://localhost:9003

Redis             redis://localhost:6379

PostgreSQL        localhost:5432

## Production-Style Deployment

A production-style Docker setup is included for cloud readiness:

docker compose -f docker-compose.prod.yml up --build
This runs:

Django with Gunicorn

Independent Celery workers

Redis, PostgreSQL, MinIO

## Storage & Database

PostgreSQL
Stores:

Image metadata

Import job status

MinIO (S3-compatible)
Stores:

Uploaded images

## API Usage Examples

All API examples are also provided in:

api_examples.md

## Frontend & Backend Commands

## Backend Commands

Navigate to backend

cd services/django-api

Copy environment variables

cp .env.example .env

Run database migrations

docker compose exec django python manage.py migrate

## (Optional) Run Celery workers manually

For import tasks
celery -A core worker -l info -Q importer

For upload tasks
celery -A core worker -l info -Q uploader

Start backend & all services (dev mode)
docker compose up --build

Start backend & all services (production)
docker compose -f docker-compose.prod.yml up --build

## Frontend Commands

Navigate to frontend
cd frontend

Install dependencies
npm install

Run frontend in development mode
npm run dev

## Opens at http://localhost:3000

## Build frontend for production

npm run build
npm run preview
