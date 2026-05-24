import requests
import time
import re
import datetime


class Scraper:

    def __init__(
        self,
        domain="www.cpubenchmark.net"
    ):

        if domain not in [

            "www.cpubenchmark.net",

            "www.videocardbenchmark.net",

            "www.harddrivebenchmark.net"

        ]:

            raise ValueError(
                "Invalid domain"
            )

        self.domain = domain

        self.url = {

            "www.cpubenchmark.net":
            (
                "https://www.cpubenchmark.net/"
                "CPU_mega_page.html"
            ),

            "www.videocardbenchmark.net":
            (
                "https://www.videocardbenchmark.net/"
                "GPU_mega_page.html"
            ),

            "www.harddrivebenchmark.net":
            (
                "https://www.harddrivebenchmark.net/"
                "hdd-mega-page.html"
            )

        }[domain]

        self.scrape()

    def scrape(self):

        session = requests.Session()

        headers = {

            "User-Agent":
            (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/136.0 Safari/537.36"
            ),

            "Accept-Language":
            "en-US,en;q=0.9",

            "Referer":
            self.url,

            "X-Requested-With":
            "XMLHttpRequest",

            "Accept":
            (
                "application/json,"
                " text/javascript,"
                " */*; q=0.01"
            )
        }

        # Lấy cookie trước

        session.get(

            self.url,

            headers=headers,

            timeout=30

        )

        # Gọi API data

        api_url = (

            f"https://{self.domain}/data/"
            f"?_={int(time.time()*1000)}"

        )

        response = session.get(

            api_url,

            headers=headers,

            timeout=30

        )

        response.raise_for_status()

        data = response.json()

        self.items = data["data"]

        return self.items

    def get_item(
        self,
        item_id
    ):

        for item in self.items:

            if str(item["id"]) == str(item_id):

                return item

        return None

    def search(
        self,
        keyword
    ):

        keyword = keyword.lower()

        result = []

        for item in self.items:

            if keyword in item["name"].lower():

                result.append(item)

        return result