import sqlite3
from bs4 import BeautifulSoup
from requests_cache import CachedSession
from time import sleep


def db_connect():
    return sqlite3.connect(r"db\onedata_db.db")


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


def scrape(conn: sqlite3.Connection, mulai: int, selesai: int, interval: int = 0):
    cursor = conn.cursor()
    domain = r"https://katalog.data.go.id"
    scraped_link = []
    for halaman in range(mulai, selesai):
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
        sleep(interval)


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
