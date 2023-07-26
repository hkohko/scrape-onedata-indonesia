import sqlite3
import sys
import os
from bs4 import BeautifulSoup
from requests_cache import CachedSession
from time import sleep
from src.max_page import get_maxpage
from src.page_history import insert_into_page_history

if not os.path.exists(r"db/"):
    os.makedirs("db/")

conn = sqlite3.connect(r"db\onedata_db.db")
args = sys.argv


def create_table(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS halaman_web("
        "halaman INTEGER,"
        "link TEXT, "
        "PRIMARY KEY(link)"
        ")"
        "STRICT"
    )


def scrape(conn: sqlite3.Connection, end_: int):
    cursor = conn.cursor()
    if len(start_) == 1:
        sleep_ = 0
    else:
        sleep_ = float(sys.argv[1])
    domain = r"https://katalog.data.go.id"
    scraped_link = []
    for halaman in range(1, end_):
        print(f"halaman: {halaman}")
        url = f"https://katalog.data.go.id/dataset/?page={halaman}"
        session = CachedSession("scrape_links")
        response = (session.get(url)).text
        soup = BeautifulSoup(response, "lxml")
        divs = soup.find_all("div", {"class": "module-content"})
        for div in divs:
            h2s = div.find_all("h2", {"class": "dataset-heading"})
            for h2 in h2s:
                page = h2.find("a", {"href": True})["href"]
                link = domain + page
                scraped_link.append((halaman, link))
        print(f"jumlah link: {halaman*20}")
        print(f"halaman {halaman} selesai")
        print("menulis ke database...")
        insert_into_db(conn, scraped_link)
        print("selesai!")
        scraped_link.clear()
        sleep(sleep_)


def insert_into_db(conn, data):
    Q_INSERT_LAMAN = """INSERT OR IGNORE INTO halaman_web(
    halaman,
    link
    ) VALUES(
    ?,
    ?
    )
    """
    with conn:
        cursor = conn.cursor()
        cursor.executemany(Q_INSERT_LAMAN, data)
        conn.commit()


if __name__ == "__main__":
    create_table(conn)
