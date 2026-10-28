import json
import os
import sqlite3
from datetime import UTC, datetime

# Vercel serverless has a read-only filesystem except for /tmp
# So we use /tmp/history.db if we are on Vercel
IS_VERCEL = os.environ.get("VERCEL") == "1"
if IS_VERCEL:
    DB_PATH = "/tmp/history.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "history.db")


def init_db() -> None:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS crawl_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                brand_name TEXT,
                timestamp TEXT,
                visibility_score INTEGER,
                opportunity_score INTEGER,
                result_payload TEXT
            )
            """
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to init DB at {DB_PATH}: {e}")


def save_crawl(
    url: str,
    brand_name: str,
    visibility_score: int,
    opportunity_score: int,
    result_payload: dict,
) -> None:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        timestamp = datetime.now(UTC).isoformat()
        cursor.execute(
            """
            INSERT INTO crawl_history (url, brand_name, timestamp, visibility_score, opportunity_score, result_payload)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                url,
                brand_name,
                timestamp,
                visibility_score,
                opportunity_score,
                json.dumps(result_payload),
            ),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to save to DB at {DB_PATH}: {e}")


def get_history(url: str | None = None) -> list[dict]:
    """Retrieve authentic audit history from database. Never returns fake/mock data."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if url:
            cursor.execute(
                "SELECT * FROM crawl_history WHERE url = ? ORDER BY timestamp DESC",
                (url,),
            )
        else:
            cursor.execute(
                "SELECT * FROM crawl_history ORDER BY timestamp DESC LIMIT 50"
            )
        rows = cursor.fetchall()
        conn.close()

        results = []
        for row in rows:
            try:
                payload = json.loads(row["result_payload"])
            except Exception:
                payload = {}
            results.append(
                {
                    "id": row["id"],
                    "url": row["url"],
                    "brand_name": row["brand_name"],
                    "timestamp": row["timestamp"],
                    "visibility_score": row["visibility_score"],
                    "opportunity_score": row["opportunity_score"],
                    "result_payload": payload,
                }
            )

        return results
    except Exception as e:
        print(f"Failed to read from DB at {DB_PATH}: {e}")
        return []


init_db()
