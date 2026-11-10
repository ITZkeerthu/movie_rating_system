"""Route tests that run against an in-memory SQLite database (no PostgreSQL needed).

Run from the backend/ directory:  python -m pytest tests
"""
import os
import sys

os.environ["DATABASE_URL"] = "sqlite://"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402

from app import app  # noqa: E402
from models import Movie, db  # noqa: E402


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all([
            Movie(title="Alpha", release_year=2001, genre="Drama", imdb_rating=8.0),
            Movie(title="Beta", release_year=2010, genre="Comedy", imdb_rating=6.0),
        ])
        db.session.commit()
    with app.test_client() as c:
        yield c


def register(client, name="u1"):
    r = client.post("/auth/register", json={
        "username": name, "email": f"{name}@example.com", "password": "pw12345"})
    assert r.status_code == 201
    return {"Authorization": "Bearer " + r.get_json()["token"]}


def test_register_rejects_non_json_body(client):
    r = client.post("/auth/register", data="not json", content_type="text/plain")
    assert r.status_code == 400


def test_register_missing_fields_and_duplicate(client):
    assert client.post("/auth/register", json={"username": "x"}).status_code == 400
    register(client)
    r = client.post("/auth/register", json={
        "username": "u1", "email": "u1@example.com", "password": "pw12345"})
    assert r.status_code == 409


def test_login_wrong_password(client):
    register(client)
    r = client.post("/auth/login", json={"email": "u1@example.com", "password": "bad"})
    assert r.status_code == 401


def test_movies_limit_is_clamped(client):
    assert client.get("/movies?limit=-5").get_json()["total_count"] == 2
    assert client.get("/movies?limit=abc").get_json()["total_count"] == 2
    assert client.get("/movies?limit=1").get_json()["total_count"] == 1


def test_movies_filter_by_genre(client):
    titles = [m["title"] for m in client.get("/movies?genre=comedy").get_json()["movies"]]
    assert titles == ["Beta"]


def test_watchlist_status_uses_integer_user_id(client):
    h = register(client)
    assert client.post("/watchlist/1", headers=h).status_code == 201
    r = client.get("/watchlist/status?movie_ids=1,2", headers=h)
    assert r.status_code == 200
    assert r.get_json()["status"] == {"1": True, "2": False}
    assert client.get("/watchlist/status?movie_ids=a", headers=h).status_code == 400
