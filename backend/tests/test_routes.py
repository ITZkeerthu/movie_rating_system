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


def test_movies_search_treats_wildcards_literally(client):
    assert client.get("/movies?search=%25").get_json()["total_count"] == 0
    assert client.get("/movies?search=_lpha").get_json()["total_count"] == 0
    assert client.get("/movies?search=alp").get_json()["total_count"] == 1
    assert client.get("/movies?genre=%25").get_json()["total_count"] == 0


def test_auth_rejects_non_string_fields(client):
    r = client.post("/auth/register", json={
        "username": "u2", "email": "u2@example.com", "password": 12345})
    assert r.status_code == 400
    r = client.post("/auth/login", json={"email": ["a"], "password": {"x": 1}})
    assert r.status_code == 400


def test_watchlist_add_list_remove_roundtrip(client):
    h = register(client)
    assert client.post("/watchlist/1", headers=h).status_code == 201
    # Adding twice is a no-op that reports the movie is already present
    dup = client.post("/watchlist/1", headers=h)
    assert dup.status_code == 200
    assert dup.get_json()["success"] is False

    listing = client.get("/watchlist", headers=h).get_json()
    assert listing["total_count"] == 1
    assert listing["watchlist"][0]["title"] == "Alpha"
    assert listing["watchlist"][0]["in_watchlist"] is True

    assert client.delete("/watchlist/1", headers=h).status_code == 200
    assert client.get("/watchlist", headers=h).get_json()["total_count"] == 0
    # Removing something that is no longer there is a 404
    assert client.delete("/watchlist/1", headers=h).status_code == 404


def test_watchlist_unknown_movie_returns_404(client):
    h = register(client)
    assert client.post("/watchlist/999", headers=h).status_code == 404
    assert client.delete("/watchlist/999", headers=h).status_code == 404


def test_watchlist_requires_auth_and_is_per_user(client):
    assert client.get("/watchlist").status_code == 401
    h1 = register(client, "u1")
    h2 = register(client, "u2")
    client.post("/watchlist/1", headers=h1)
    assert client.get("/watchlist", headers=h1).get_json()["total_count"] == 1
    assert client.get("/watchlist", headers=h2).get_json()["total_count"] == 0


def test_me_returns_current_user_and_requires_token(client):
    assert client.get("/auth/me").status_code == 401
    h = register(client)
    body = client.get("/auth/me", headers=h).get_json()
    assert body["username"] == "u1"
    assert body["email"] == "u1@example.com"
    assert "password" not in body and "password_hash" not in body


def test_movies_rating_year_and_sort_filters(client):
    def titles(qs):
        return [m["title"] for m in client.get("/movies" + qs).get_json()["movies"]]

    assert titles("?min_rating=7") == ["Alpha"]
    assert titles("?max_rating=7") == ["Beta"]
    assert titles("?year=2010") == ["Beta"]
    assert titles("?sort=year_asc") == ["Alpha", "Beta"]
    assert titles("?sort=year_desc") == ["Beta", "Alpha"]
    assert titles("?sort=title_asc") == ["Alpha", "Beta"]
    # Unknown sort values fall back to rating_desc instead of erroring
    assert titles("?sort=bogus") == ["Alpha", "Beta"]


def test_watchlist_status_rejects_too_many_ids(client):
    h = register(client)
    ids = ",".join(str(i) for i in range(1, 202))
    assert client.get(f"/watchlist/status?movie_ids={ids}", headers=h).status_code == 400
    ids = ",".join(str(i) for i in range(1, 201))
    assert client.get(f"/watchlist/status?movie_ids={ids}", headers=h).status_code == 200


def test_cors_origins_env_is_honoured(client):
    r = client.options("/movies", headers={
        "Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"})
    assert r.headers.get("Access-Control-Allow-Origin") == "http://localhost:3000"
