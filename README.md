📘 README.md

📝 BackendMedia

A backend platform to manage media content with user authentication.  
This repository contains the full FastAPI backend to manage media uploads, users, and streaming URLs.

📂 Project Structure

BackendMedia/
├── main.py             # FastAPI app entrypoint
├── models.py           # Database models
├── database.py         # DB connection and setup
├── auth.py             # Authentication routes
├── media.py            # Media routes
├── requirements.txt    # Python dependencies
├── venv/               # Virtual environment

🚀 Features

- User signup and login with JWT authentication
- Add and manage media entries
- Generate streaming URLs for media
- Password hashing using bcrypt

🛠️ Tech Stack

- Python 3.13
- FastAPI 0.116.1
- SQLAlchemy 2.0
- Uvicorn 0.35.0
- JWT Authentication
- Passlib + bcrypt
- SQLite3 (default DB for development)

✅ Current Status

- [x] Project initialized
- [x] Git repo cleaned and pushed to GitHub
- [x] FastAPI app created with auth and media routes
- [x] Tested endpoints locally

🧪 How to Run Locally

powershell
# Clone the repo
git clone https://github.com/kamranNabil/BackendMedia.git
cd BackendMedia

# Create a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn main:app --reload --log-level debug

The API will be available at `http://127.0.0.1:8000`.

📬 Feedback & Contributions
Pull requests and issues are welcome.  
Feel free to fork and enhance the project!

📃 License

This project is open source and available under the [MIT License](LICENSE).
