from bs4 import BeautifulSoup
import sqlite3
import requests
from requests import exceptions
import sys
from time import sleep

conn = sqlite3.connect(r"db\onedata_db.db")


def create_table(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS json_api("
        "link TEXT,"
        "json_link TEXT PRIMARY KEY"
        ")"
        "STRICT"
    )


def scrape(conn: sqlite3.Connection):
    if len(sys.argv) == 1:
        start_ = 1
        sleep_ = 1
    else:
        start_ = int(sys.argv[1])
        sleep_ = float(sys.argv[2])
    cursor = conn.cursor()
    max_halaman_web = cursor.execute("SELECT MAX(rowid) FROM halaman_web")
    for data in max_halaman_web:
        max_value = int(data[0])
    max_json_link = cursor.execute("SELECT MAX(rowid) FROM json_api")
    for num in max_json_link:
        last_json = int(num[0])
    for index in range(last_json, max_value + 1):
        data = cursor.execute(
            "SELECT rowid, link FROM halaman_web WHERE rowid=?", (index,)
        )
        scraped_json_link = []
        for rowid, link in data:
            print(f"rowid: {rowid}")
            json_link = scrape_json(link)
            scraped_json_link.append((link, json_link))
            print("selesai!")
            print("menulis ke db...")
            insert_into_db(conn, scraped_json_link)
            print("selesai!")
            scraped_json_link.clear()
            sleep(sleep_)


def scrape_json(link: str):
    print(f"link: {link}")
    while True:
        try:
            response = requests.get(link).text
            soup = BeautifulSoup(response, "lxml")
            uls = soup.find("ul", {"class": "list-group"})
            if uls is None:
                return "None"
            json_link = uls.find("a", {"href": True})["href"]  # json api
            return json_link
        except (
            exceptions.ConnectTimeout,
            exceptions.ReadTimeout,
            exceptions.Timeout,
            TimeoutError,
        ):
            for i in range(0, 60):
                print(f"ConnectTimeOut, will retry in {60-i}s", end=" \r")
                sleep(1)
            continue
            # scrape_json(halaman, link)


def insert_into_db(conn: sqlite3.Connection, data: list[tuple]):
    Q_INSERT_JSON = """INSERT OR IGNORE INTO json_api(
    link,
    json_link
    ) VALUES(
    ?,
    ?
    )
    """
    with conn:
        cursor = conn.cursor()
        cursor.executemany(Q_INSERT_JSON, data)
        conn.commit()


if __name__ == "__main__":
    create_table(conn)
