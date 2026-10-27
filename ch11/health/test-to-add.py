# Add to the end of ch05/tests/test_notes_api.py, before the route exists,
# and run it to see it fail (404 instead of 200).


def test_health_reports_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
