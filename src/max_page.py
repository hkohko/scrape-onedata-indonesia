from bs4 import BeautifulSoup
from requests_cache import CachedSession
from pprint import pprint
import re


def get_maxpage():
    url = r"https://katalog.data.go.id/dataset"
    session = CachedSession("max_links")
    response = session.get(url).text

    soup = BeautifulSoup(response, "lxml")
    divs = soup.find("div", {"class": "pagination-wrapper"})
    max_page = divs.find_all("a", {"href": True})
    pattern = r">(\d+)<"
    page_list = []
    for page in max_page:
        page_num = re.search(pattern, str(page), re.IGNORECASE)
        if page_num is not None:
            page_list.append(int(page_num.group(1)))
    return max(page_list)
