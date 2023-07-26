import sqlite3
from requests_cache import CachedSession
from pprint import pprint

conn = sqlite3.connect("onedata_db.db")

session = CachedSession("req_cache")
url = r"https://katalog.data.go.id/api/action/package_show?id=84c3fe40-85dd-494a-b398-48ad0f025e0b"
url2 = r"https://katalog.data.go.id/api/action/package_show?id=08ff3baa-584c-4df9-bba1-fb9ece7d7a4d"
url3 = r"https://katalog.data.go.id/api/action/package_show?id=ca083033-9590-4127-8c3c-5e3e3d091c40"
response: dict = session.get(url2).json()
result: dict = response.get("result")
for dictionary in result.get("extras"):
    if dictionary.get("key") == "harvest_source_title":
        source = dictionary.get("value")
resource: list = result.get("resources")
pprint(source)
pprint(resource)
