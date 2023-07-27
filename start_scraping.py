import sqlite3
import os
import sys
from collections import defaultdict
from time import sleep
from src import _initialize
from src import json_links
from src import scrape_links
from pathlib import Path

os.chdir(Path(__file__).parent)
_initialize._init()
conn = sqlite3.connect(r"db\onedata_db.db")


def arguments():
    arg_dict = defaultdict(str)
    keywords = ["mulai", "selesai", "interval"]
    valid_argument = "mulai=<angka>\nselesai=<angka>\ninterval=<angka>\n"
    args = sys.argv
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=")
            arg_dict[key.strip()] = value.strip()

    if "" in arg_dict.values() or "" in arg_dict.keys():
        sys.exit(f"\nargumen tidak lengkap:\n{valid_argument}")

    for key in arg_dict.keys():
        if key not in keywords:
            sys.exit(f"\nkeyword argument salah:\n{valid_argument}")
    try:
        for values in arg_dict.values():
            float(values)
    except ValueError:
        sys.exit(f"\nparameter bukan angka:\n{valid_argument}")

    mulai = arg_dict.get("mulai")
    selesai = arg_dict.get("selesai")
    interval = arg_dict.get("interval")

    if mulai and selesai and interval is not None:
        return abs(int(mulai)), abs(int(selesai)), abs(float(interval))
    else:
        sys.exit(f"\nargumen salah:\n{valid_argument}")


def start_scrape():
    if len(sys.argv) == 1:
        mulai = 1
        selesai = 5
        interval = 0
        print(f"Default values:\nFirst {selesai} pages\nInterval {interval}s\n")
    else:
        mulai, selesai, interval = arguments()
        print(f"\nValues:\nhalaman {mulai}-{selesai}\ninterval {interval}s\n")
    scrape_links.scrape(conn, mulai, selesai + 1, interval)
    json_links.scrape(conn, interval)


if __name__ == "__main__":
    start_scrape()
