# Exercise 11.3: one test for each limit. Add to the end of
# ch05/tests/test_notes_api.py and see both fail before the change.


def test_title_limit_is_200_chars(client):
    assert client.post("/notes", json={"title": "x" * 200}).status_code == 201
    r = client.post("/notes", json={"title": "x" * 201})
    assert r.status_code == 422
    n = make(client)
    r = client.patch(f"/notes/{n['id']}", json={"title": "x" * 201})
    assert r.status_code == 422


def test_body_limit_is_10000_chars(client):
    r = client.post("/notes", json={"title": "t", "body": "y" * 10_000})
    assert r.status_code == 201
    r = client.post("/notes", json={"title": "t", "body": "y" * 10_001})
    assert r.status_code == 422
    n = make(client)
    r = client.patch(f"/notes/{n['id']}", json={"body": "y" * 10_001})
    assert r.status_code == 422
