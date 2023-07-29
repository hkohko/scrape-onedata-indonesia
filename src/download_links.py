import sqlite3
import os
import json
import requests
from time import sleep
from tqdm import tqdm
from requests import exceptions
from pprint import pprint
from pathlib import Path

os.chdir(Path(__file__).parent.parent)
conn = sqlite3.connect("db/onedata_db.db")


def create_table(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS json_metadata("
        "json_api_rowid INTEGER,"
        "sumber_data TEXT,"
        "nama_file TEXT,"
        "deskripsi TEXT,"
        "link_download TEXT PRIMARY KEY"
        ")"
        "STRICT"
    )


def start_scraping(conn: sqlite3.Connection):
    cursor = conn.cursor()
    json_links: int = cursor.execute("SELECT MAX(rowid) FROM json_api")
    for num_json in json_links:
        if num_json[0] is None:
            json_links_max = 0
        else:
            json_links_max = int(num_json[0])
    json_metadata: int = cursor.execute("SELECT MAX(json_api_rowid) FROM json_metadata")
    for num_metadata in json_metadata:
        if num_metadata[0] is None:
            json_metadata_last = 0
        else:
            json_metadata_last = int(num_metadata[0])
    for index in range(json_metadata_last, json_links_max + 1):
        json_links = cursor.execute(
            "SELECT rowid, json_link FROM json_api WHERE rowid=?", (index,)
        )
        result_api_call = []
        for rowid, json_link in tqdm(json_links, desc=f"rowid: {index}"):
            api_call_data = api_call(json_link)
            for sumber_data, nama_file, deskripsi, link_dl in tqdm(
                api_call_data, desc="fetching data"
            ):
                result_api_call.append(
                    {
                        "json_api_rowid": rowid,
                        "sumber": sumber_data,
                        "nama": nama_file,
                        "deskripsi": deskripsi,
                        "link": link_dl,
                    }
                )
                insert_into_json_metadata(conn, result_api_call)
            result_api_call.clear()


def api_call(json_link):
    while True:
        try:
            r = requests.get(json_link)
            break
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
    response: dict = r.json()
    result: dict = response.get("result", "")
    metadata: list = result.get("resources", "")
    if len(metadata) == 0:
        return "", "", "", ""
    if len(result.get("extras")) == 0:
        sumber_data = ""
    else:
        for dictionary in result.get("extras"):
            key = dictionary.get("key")
            if key == "harvest_source_title" and key is not None:
                sumber_data = dictionary.get("value", "")  # data 1
            else:
                sumber_data = ""
    for data in metadata:
        nama_file: str = data.get("name", "")  # data 2
        deskripsi: str = data.get("description", "")  # data 3
        link_download: str = data.get("url", "")  # data 4
        yield sumber_data, nama_file, deskripsi, link_download


def insert_into_json_metadata(conn: sqlite3.Connection, data):
    Q_INSERT_INTO_JSON_METADATA = """INSERT OR IGNORE INTO json_metadata(
    json_api_rowid,
    sumber_data,
    nama_file,
    deskripsi,
    link_download
    ) VALUES(
    :json_api_rowid,
    :sumber,
    :nama,
    :deskripsi,
    :link
    )
    """
    with conn:
        cursor = conn.cursor()
        cursor.executemany(Q_INSERT_INTO_JSON_METADATA, data)
        conn.commit()


if __name__ == "__main__":
    # create_table(conn)
    start_scraping(conn)
