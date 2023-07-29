import sqlite3
import requests
import sys
import os
from bs4 import BeautifulSoup
from requests import exceptions
from time import sleep
from tqdm import tqdm


def db_connect():
    return sqlite3.connect(r"db\onedata_db.db")


def create_table(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS json_api("
        "link TEXT,"
        "json_link TEXT PRIMARY KEY"
        ")"
        "STRICT"
    )


def iterate_db(conn: sqlite3.Connection, sleep_: int = 0):
    cursor = conn.cursor()
    max_halaman_web = cursor.execute("SELECT MAX(rowid) FROM halaman_web")
    for data in max_halaman_web:
        max_value = int(data[0])
    max_json_link = cursor.execute("SELECT MAX(rowid) FROM json_api")
    for num in max_json_link:
        if num[0] is None:
            last_json = 0
        else:
            last_json = int(num[0])
    for index in range(last_json, max_value + 1):
        data = cursor.execute(
            "SELECT rowid, link FROM halaman_web WHERE rowid=?", (index,)
        )
        scraped_json_link = []
        for rowid, link in tqdm(data, desc=f"rowid: {index}"):
            json_link = scrape_json(link)
            scraped_json_link.append((link, json_link))
            insert_into_db(conn, scraped_json_link)
            scraped_json_link.clear()
            sleep(sleep_)


def scrape_json(link: str):
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
    iterate_db(db_connect())
