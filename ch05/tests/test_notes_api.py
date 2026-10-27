"""Tests for the Notes API in ../notes_api.py."""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import notes_api  # noqa: E402  (the real module, not a copy)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Return a test client backed by a fresh SQLite file."""
    monkeypatch.setattr(notes_api, "DB_PATH", tmp_path / "notes.db")
    notes_api.init_db()
    return TestClient(notes_api.app)


def make(client, title="t", body="b"):
    """Create a note and return its JSON."""
    r = client.post("/notes", json={"title": title, "body": body})
    assert r.status_code == 201
    return r.json()


def test_create_returns_201_and_the_note(client):
    r = client.post("/notes", json={"title": "hello", "body": "world"})
    assert r.status_code == 201
    note = r.json()
    assert note["id"] == 1
    assert note["title"] == "hello"
    assert note["body"] == "world"
    assert note["created_at"] == note["updated_at"]


def test_blank_title_is_422(client):
    r = client.post("/notes", json={"title": "   ", "body": "b"})
    assert r.status_code == 422


def test_missing_title_is_422(client):
    r = client.post("/notes", json={"body": "b"})
    assert r.status_code == 422


def test_list_empty(client):
    r = client.get("/notes")
    assert r.status_code == 200
    assert r.json() == []


def test_list_returns_all_notes(client):
    make(client, "first")
    make(client, "second")
    r = client.get("/notes")
    assert r.status_code == 200
    assert [n["title"] for n in r.json()] == ["first", "second"]


def test_get_one(client):
    note = make(client, "hello", "world")
    r = client.get(f"/notes/{note['id']}")
    assert r.status_code == 200
    assert r.json() == note


def test_search_matches_title(client):
    make(client, "alpha", "one")
    make(client, "beta", "two")
    r = client.get("/notes", params={"q": "alp"})
    assert r.status_code == 200
    assert [n["title"] for n in r.json()] == ["alpha"]


def test_search_matches_body_only(client):
    make(client, "groceries", "buy milk")
    r = client.get("/notes", params={"q": "milk"})
    assert [n["title"] for n in r.json()] == ["groceries"]


def test_get_missing_is_404_with_spec_body(client):
    r = client.get("/notes/999")
    assert r.status_code == 404
    assert r.json() == {"error": "not found"}


def test_patch_updates_only_given_fields(client):
    note = make(client, "title", "old")
    r = client.patch(f"/notes/{note['id']}", json={"body": "new"})
    assert r.status_code == 200
    assert r.json()["title"] == "title"
    assert r.json()["body"] == "new"


def test_patch_missing_is_404(client):
    r = client.patch("/notes/999", json={"body": "new"})
    assert r.status_code == 404
    assert r.json() == {"error": "not found"}


def test_delete_returns_204_then_get_is_404(client):
    note = make(client)
    r = client.delete(f"/notes/{note['id']}")
    assert r.status_code == 204
    assert client.get(f"/notes/{note['id']}").status_code == 404


def test_search_treats_wildcards_literally(client):
    make(client, "alpha")
    make(client, "100% done")
    r = client.get("/notes", params={"q": "%"})
    assert [n["title"] for n in r.json()] == ["100% done"]
