import requests

from crawlers.gearvn.categories import GEARVN_APIS


class GearVNCrawler:

    def get_products(self, category):

        all_products = []

        page = 1

        while True:

            url = (
                f"{GEARVN_APIS[category]}"
                f"?page={page}"
            )

            response = requests.get(
                url,
                timeout=30
            )

            response.raise_for_status()

            products = response.json()["products"]

            if not products:
                break

            print(
                f"[{category}] "
                f"page number {page}: "
                f"{len(products)} products"
            )

            all_products.extend(products)

            page += 1

        return all_products