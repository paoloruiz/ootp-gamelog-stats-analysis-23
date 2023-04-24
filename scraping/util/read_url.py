from urllib.error import HTTPError
import urllib.request
import random
from time import sleep
import gzip


headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip",
    "Host": "35.190.82.228"
}

def __random_sleep__():
    #sleep(5 + 1 * random.random())
    sleep(5)

def get_html_from_url_canned(url: str) -> str:
    with open("scraping/canned_responses/" + url, "r") as f:
        return f.read()

def get_html_from_url_full_req(url: str) -> str:
    __random_sleep__()

    print("requesting", url)
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as response:
            if response.getcode() == 200:
                return gzip.decompress(response.read())
    except HTTPError:
        pass
    return None