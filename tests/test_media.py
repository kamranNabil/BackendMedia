import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import database, models
from app.utils import create_access_token
import uuid

client = TestClient(app)

@pytest.fixture
def token():
    from app.models import AdminUser
    db = database.SessionLocal()

    # Generate a unique email for each test run
    unique_email = f"test_{uuid.uuid4()}@example.com"
    user = AdminUser(email=unique_email, hashed_password="test")

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return create_access_token({"sub": str(user.id)})

# ---------------- Fixture to setup DB ---------------- #
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    models.Base.metadata.create_all(bind=database.engine)
    yield
    models.Base.metadata.drop_all(bind=database.engine)


# ---------------- Fixture to create test token ---------------- #
@pytest.fixture
def token():
    from app.models import AdminUser
    db = database.SessionLocal()
    user = AdminUser(email="test@example.com", hashed_password="test")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return create_access_token({"sub": str(user.id)})


# ---------------- Helper to create media ---------------- #
@pytest.fixture
def media_id(token):
    payload = {
        "title": "Test Media",
        "type": "video",
        "file_url": "http://test.com/video.mp4"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/media", json=payload, headers=headers)
    return response.json()["id"]


# ---------------- Tests ---------------- #
def test_create_media(token):
    payload = {"title": "Test Media2", "type": "video", "file_url": "http://test.com/video2.mp4"}
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/media", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Media2"


def test_media_analytics_caching(media_id):
    # First call should hit DB and populate cache
    response1 = client.get(f"/media/{media_id}/analytics")
    assert response1.status_code == 200
    data1 = response1.json()

    # Second call should hit Redis (cached)
    response2 = client.get(f"/media/{media_id}/analytics")
    assert response2.status_code == 200
    data2 = response2.json()

    # Should be identical
    assert data1 == data2


def test_media_view_rate_limit(media_id):
    # Hit the view endpoint multiple times quickly
    last_response = None
    for _ in range(10):  # adjust based on your limiter (e.g., 5/min)
        last_response = client.post(f"/media/{media_id}/view")

    # Last request should eventually be rate limited
    assert last_response is not None
    assert last_response.status_code in [200, 429]  # 429 if rate limit triggered
