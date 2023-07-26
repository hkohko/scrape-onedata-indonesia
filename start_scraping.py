from src import json_links
from src import scrape_links
from src.page_history import insert_into_page_history
from src.max_page import get_maxpage
import sqlite3
import os
from pathlib import Path

os.chdir(Path(__file__).parent)
if not os.path.exists("db"):
    os.makedirs("db")
conn = sqlite3.connect(r"db\onedata_db.db")

if __name__ == "__main__":
    cursor = conn.cursor()
    live_max_page: int = get_maxpage()
    for last_page in cursor.execute("SELECT MAX(halaman_terakhir) FROM page_history"):
        db_last_page = last_page[0]
    if live_max_page > db_last_page:
        scrape_links.scrape(conn, live_max_page - db_last_page + 1)
    else:
        print("db uptodate")
    insert_into_page_history(conn)
    json_links.scrape(conn)
