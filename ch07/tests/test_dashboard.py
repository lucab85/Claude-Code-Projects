"""Structural checks for the dashboard page in ../app.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import app  # noqa: E402


def get_page():
    """Return the HTML of the dashboard page."""
    response = app.test_client().get("/")
    assert response.status_code == 200
    return response.get_data(as_text=True)


def test_has_three_kpi_cards():
    assert get_page().count('<article class="kpi">') == 3


def test_table_has_five_rows():
    body = get_page().split("<tbody>")[1].split("</tbody>")[0]
    assert body.count("<tr>") == 5


def test_sidebar_has_five_links():
    nav = get_page().split('<nav class="sidebar">')[1].split("</nav>")[0]
    assert nav.count("<li") == 5


def test_footer_shows_version():
    assert '<footer class="footer">v1.0.0</footer>' in get_page()
