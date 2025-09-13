# db.py
import psycopg2
from contextlib import contextmanager

@contextmanager
def db_cursor():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="123456"
    )
    try:
        with conn:                 # begins a txn; commits/rolls back on exit
            with conn.cursor() as cur:  # cursor auto-closes on exit
                yield cur
    finally:
        conn.close()               # connection ALWAYS closed
