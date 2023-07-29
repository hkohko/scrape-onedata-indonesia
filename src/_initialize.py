from pathlib import Path
from src import json_links
from src import scrape_links
from src import download_links
import os
import sqlite3


def _init():
    os.chdir(Path(__file__).parent.parent)
    if not os.path.exists(r"db/"):
        os.makedirs("db/")

    conn = sqlite3.connect("db\onedata_db.db")

    scrape_links.create_table(conn)
    json_links.create_table(conn)
    download_links.create_table(conn)
