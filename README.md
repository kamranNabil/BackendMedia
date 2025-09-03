# BackendMedia

A media platform backend built with **FastAPI**, featuring Redis caching, rate limiting, authentication, and Dockerized deployment.

---

## Features

- User authentication (`signup` & `login`) with JWT tokens
- CRUD operations for media assets
- Redis caching for `GET /media/:id/analytics`
- Rate limiting for `POST /media/:id/view`
- SQLite database for development (can switch to other DBs)
- Fully tested using **PyTest**
- Dockerized for easy setup

---

## Requirements

- Python 3.11+
- Docker & Docker Compose
- Redis
- Git

---

## Project Structure

BackendMedia/
├─ app/
│ ├─ init.py
│ ├─ main.py
│ ├─ auth.py
│ ├─ database.py
│ ├─ models.py
│ ├─ media.py
│ ├─ redis_client.py
│ ├─ utils.py
│ └─ limiter.py
├─ tests/
│ └─ test_media.py
├─ Dockerfile
├─ docker-compose.yaml
├─ requirements.txt
├─ .env.example
└─ README.md

## Setup

1. **Clone the repository**

git clone https://github.com/kamranNabil/BackendMedia.git
cd BackendMedia
Create virtual environment

python -m venv venv
source venv/Scripts/Activate.ps1  # Windows PowerShell
Install dependencies

pip install -r requirements.txt
Copy .env.example to .env and update variables

cp .env.example .env
# Edit .env as needed
Run the server

uvicorn app.main:app --reload
Access the API documentation

http://127.0.0.1:8000/docs
Docker Setup
Build the Docker image

docker build -t media-backend .
Run the Docker container

docker run -p 8000:8000 media-backend
Optional: Use docker-compose if defined in docker-compose.yaml

docker-compose up --build
Running Tests

pytest tests/
API Endpoints
Auth

POST /auth/signup – Register new user

POST /auth/login – Login and receive JWT token

Media

POST /media – Create a media item

GET /media/{id}/stream-url – Get secure stream URL

GET /media/{id}/analytics – Get media analytics (Redis cached)

POST /media/{id}/view – Increment media views (rate-limited)

License

This project is licensed under MIT License.
