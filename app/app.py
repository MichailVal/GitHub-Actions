import os
import psycopg2

from flask import Flask, jsonify

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )


def fetch_items():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, name FROM items ORDER BY id;")
        return cur.fetchall()


@app.get("/health")
def health():
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1;")
        return jsonify(status="ok", database="connected"), 200
    except Exception as exc:
        return jsonify(status="error", database=str(exc)), 503


@app.get("/api/data")
def api_data():
    items = fetch_items()
    return jsonify([{"id": i, "name": n} for i, n in items])


@app.get("/api/items/count")
def api_items_count():
    return str(len(fetch_items())), 200, {"Content-Type": "text/plain"}


@app.get("/")
def index():
    items = fetch_items()
    rows = "".join(f"<li>{n}</li>" for _, n in items)
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>Items</title></head><body>"
        "<h1>Items</h1>"
        f"<p>Total: <span id=\"items-count\">{len(items)}</span></p>"
        f"<ul>{rows}</ul>"
        "</body></html>"
    )
