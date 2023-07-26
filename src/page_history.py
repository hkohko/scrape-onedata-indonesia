import sqlite3
import os
from src.max_page import get_maxpage
from collections import namedtuple
from datetime import datetime

if not os.path.exists(r"db/"):
    os.makedirs("db/")
conn = sqlite3.connect(r"db\onedata_db.db")


def create_table_page_history(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS page_history("
        "waktu_utc TEXT,"
        "halaman_terakhir INTEGER PRIMARY KEY"
        ")"
        "STRICT"
    )


def insert_into_page_history(conn: sqlite3.Connection):
    current_time = str(datetime.utcnow())
    cursor = conn.cursor()
    last_page: int = get_maxpage()
    data = namedtuple("data", "waktu_utc halaman_tearkhir")
    page_history = data(current_time, last_page)
    Q_INSERT_INTO_PAGE_HISTORY = """INSERT OR IGNORE INTO page_history(
    waktu_utc,
    halaman_terakhir
    ) VALUES(
    ?,
    ?
    )"""

    cursor.execute(Q_INSERT_INTO_PAGE_HISTORY, page_history)
    conn.commit()


if __name__ == "__main__":
    create_table_page_history(conn)
