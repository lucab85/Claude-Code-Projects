#!/usr/bin/env python3
"""Bookmarks API: FastAPI + sqlite3, single file.

Run from this folder: uvicorn bookmarks_api:app --port 8000
"""

import sqlite3
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from starlette.exceptions import HTTPException as StarletteHTTPException

DB_PATH = Path(__file__).parent / "bookmarks.db"

URL_MAX = 2048
TITLE_MAX = 200
TAG_MAX = 50
ALLOWED_SCHEMES = ("http", "https")


@contextmanager
def get_db():
    """Open a connection, commit or roll back, and always close it."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Create the table if it doesn't exist yet."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                url        TEXT    NOT NULL,
                title      TEXT    NOT NULL,
                tag        TEXT    NOT NULL,
                created_at TEXT    NOT NULL
            )
        """)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(StarletteHTTPException)
async def http_error(request, exc):
    """Return dict details as the body itself."""
    if isinstance(exc.detail, dict):
        return JSONResponse(exc.detail, status_code=exc.status_code)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


# ---------- schemas ----------

class BookmarkIn(BaseModel):
    url: str = Field(max_length=URL_MAX)
    title: str = Field(max_length=TITLE_MAX)
    tag: str = Field(max_length=TAG_MAX)

    @field_validator("url")
    @classmethod
    def url_is_web_address(cls, v: str) -> str:
        if any(c.isspace() for c in v):
            raise ValueError("url must not contain whitespace")
        parts = urlsplit(v)
        if parts.scheme.lower() not in ALLOWED_SCHEMES or not parts.hostname:
            raise ValueError("url must be an absolute http or https URL")
        return v

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title must not be blank")
        return v

    @field_validator("tag")
    @classmethod
    def tag_is_one_word(cls, v: str) -> str:
        if not v or any(c.isspace() for c in v):
            raise ValueError("tag must be one word with no spaces")
        return v


class BookmarkOut(BaseModel):
    id: int
    url: str
    title: str
    tag: str
    created_at: str


# ---------- helpers ----------

def _row_to_bookmark(row: sqlite3.Row) -> BookmarkOut:
    return BookmarkOut(**dict(row))


def _fetch_one(conn: sqlite3.Connection, bookmark_id: int) -> sqlite3.Row:
    row = conn.execute(
        "SELECT * FROM bookmarks WHERE id = ?", (bookmark_id,)
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail={"error": "not found"})
    return row


# ---------- routes ----------

@app.post("/bookmarks", status_code=201, response_model=BookmarkOut)
def create_bookmark(payload: BookmarkIn):
    now = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO bookmarks (url, title, tag, created_at) "
            "VALUES (?, ?, ?, ?)",
            (payload.url, payload.title, payload.tag, now),
        )
        return _row_to_bookmark(_fetch_one(conn, cur.lastrowid))


@app.get("/bookmarks", response_model=list[BookmarkOut])
def list_bookmarks(tag: Optional[str] = Query(default=None)):
    with get_db() as conn:
        if tag is not None:
            rows = conn.execute(
                "SELECT * FROM bookmarks WHERE tag = ? ORDER BY id", (tag,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM bookmarks ORDER BY id").fetchall()
    return [_row_to_bookmark(r) for r in rows]


@app.get("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def get_bookmark(bookmark_id: int):
    with get_db() as conn:
        return _row_to_bookmark(_fetch_one(conn, bookmark_id))


@app.delete("/bookmarks/{bookmark_id}", status_code=204)
def delete_bookmark(bookmark_id: int):
    with get_db() as conn:
        _fetch_one(conn, bookmark_id)
        conn.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
