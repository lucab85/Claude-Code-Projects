"""Tests for the Bookmarks API in ../bookmarks_api.py."""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bookmarks_api  # noqa: E402  (the real module, not a copy)

NOT_FOUND = {"error": "not found"}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Return a test client backed by a fresh SQLite file."""
    monkeypatch.setattr(bookmarks_api, "DB_PATH", tmp_path / "bookmarks.db")
    bookmarks_api.init_db()
    return TestClient(bookmarks_api.app)


def make(client, url="https://example.com", title="ex", tag="misc"):
    """Create a bookmark and return its JSON."""
    r = client.post("/bookmarks", json={"url": url, "title": title, "tag": tag})
    assert r.status_code == 201, r.text
    return r.json()


# ---------- happy paths ----------

def test_create_returns_201_and_the_bookmark(client):
    b = make(client, "https://example.com/a?b=1", "Example", "misc")
    assert b["id"] == 1
    assert (b["url"], b["title"], b["tag"]) == (
        "https://example.com/a?b=1", "Example", "misc")
    assert b["created_at"].endswith("+00:00")


def test_list_returns_all_in_creation_order(client):
    make(client, title="first")
    make(client, title="second")
    r = client.get("/bookmarks")
    assert r.status_code == 200
    assert [b["title"] for b in r.json()] == ["first", "second"]


def test_tag_filter_is_exact_and_case_sensitive(client):
    make(client, title="a", tag="python")
    make(client, title="b", tag="Python")
    make(client, title="c", tag="python3")

    def titles(tag):
        r = client.get("/bookmarks", params={"tag": tag})
        assert r.status_code == 200
        return [b["title"] for b in r.json()]

    assert titles("python") == ["a"]
    assert titles("pyth") == []
    assert titles("") == []


def test_get_then_delete(client):
    b = make(client)
    assert client.get(f"/bookmarks/{b['id']}").json() == b
    r = client.delete(f"/bookmarks/{b['id']}")
    assert r.status_code == 204
    assert r.content == b""
    r = client.get(f"/bookmarks/{b['id']}")
    assert (r.status_code, r.json()) == (404, NOT_FOUND)


# ---------- errors ----------

def test_missing_id_is_404_with_spec_body(client):
    for method in ("GET", "DELETE"):
        r = client.request(method, "/bookmarks/999")
        assert (r.status_code, r.json()) == (404, NOT_FOUND), method


def test_invalid_input_is_422(client):
    bad = [
        {"url": "ftp://x", "title": "ex", "tag": "misc"},
        {"url": "javascript:alert(1)", "title": "ex", "tag": "misc"},
        {"url": "example.com", "title": "ex", "tag": "misc"},
        {"url": "https://example.com", "title": "   ", "tag": "misc"},
        {"url": "https://example.com", "title": "ex", "tag": "two words"},
        {"url": "https://example.com", "title": "ex"},
    ]
    for body in bad:
        r = client.post("/bookmarks", json=body)
        assert r.status_code == 422, body
    assert client.get("/bookmarks").json() == []


def test_url_must_have_a_host(client):
    # Found in review (REVIEW.md, finding 1): a prefix check let these in.
    for url in ("http://", "https:///path", "http:// example.com"):
        r = client.post("/bookmarks",
                        json={"url": url, "title": "ex", "tag": "misc"})
        assert r.status_code == 422, url
    assert make(client, url="HTTPS://Example.com")["url"] == "HTTPS://Example.com"


# ---------- boundaries ----------

def test_title_boundary_200_accepted_201_rejected(client):
    assert make(client, title="x" * 200)["title"] == "x" * 200
    r = client.post("/bookmarks", json={
        "url": "https://example.com", "title": "x" * 201, "tag": "misc"})
    assert r.status_code == 422
