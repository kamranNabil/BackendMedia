📘 BackendMedia

A backend platform to manage media content with secure user authentication and media streaming support.
This repository contains the full FastAPI backend for handling media uploads, authentication, and streaming URL generation.

📂 Project Structure
BackendMedia/
├── main.py             # FastAPI app entrypoint
├── models.py           # Database models
├── database.py         # DB connection and setup
├── auth.py             # Authentication routes
├── media.py            # Media routes (upload, fetch, streaming)
├── users.py            # User-related operations (profile, details)
├── schemas.py          # Pydantic models for request/response
├── utils.py            # Helper functions (JWT, password hashing, etc.)
├── requirements.txt    # Python dependencies
├── venv/               # Virtual environment

🚀 Features

🔐 Authentication

User signup & login with JWT tokens

Password hashing with bcrypt

Token verification and expiration handling

📺 Media Management

Upload and manage media entries

Fetch media details with filtering support

Generate streaming URLs for secure access

👤 User Management

User profile handling

Update user details (WIP)

⚙️ System

Clean modular structure (auth.py, media.py, users.py)

SQLite3 database with SQLAlchemy ORM

Logging and debugging enabled

🛠️ Tech Stack

Python 3.13

FastAPI 0.116.1

SQLAlchemy 2.0

Uvicorn 0.35.0

JWT Authentication

Passlib + bcrypt for password security

SQLite3 (default DB for development)

✅ Current Status

 Project initialized & GitHub repo ready

 FastAPI app setup with auth & media routes

 JWT authentication implemented

 Password hashing with bcrypt

 Database models created for users & media

 Streaming URL generation implemented

 Local testing of endpoints successful

 User profile management in progress

 Unit tests setup pending

🧪 How to Run Locally
# Clone the repo
git clone https://github.com/kamranNabil/BackendMedia.git
cd BackendMedia

# Create a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn main:app --reload --log-level debug


API available at 👉 http://127.0.0.1:8000

📬 Feedback & Contributions

Pull requests and issues are welcome 🚀
Fork, enhance, and contribute to make the project better!

📃 License

This project is open source and available under the MIT License.
