import psycopg
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("DATABASE_URL")

if not url:
    raise ValueError("DATABASE_URL is missing")

if "sslmode=" not in url:
    url += "&sslmode=require" if "?" in url else "?sslmode=require"

try:
    with psycopg.connect(url, connect_timeout=15) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print("PostgreSQL connected successfully!")
            print(cur.fetchone()[0])
except Exception as e:
    print(f"Connection failed: {type(e).__name__}: {e}")