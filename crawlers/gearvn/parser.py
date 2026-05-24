from bs4 import BeautifulSoup

class GearVNParser:

    #Parse_db.products
    def parse_product(self, raw_product):

        variant = {}

        if raw_product.get("variants"):
            variant = raw_product["variants"][0]

        image_url = None

        if raw_product.get("image"):
            image_url = raw_product["image"].get("src")

        return {

            # id sản phẩm GearVN
            "product_id":
                str(raw_product.get("id")),

            # mã SKU
            "sku":
                variant.get("sku"),

            # tên sản phẩm
            "title":
                raw_product.get("title"),

            # hãng
            "vendor":
                raw_product.get("vendor"),

            # loại sản phẩm
            "product_type":
                raw_product.get("product_type"),

            # slug url
            "handle":
                raw_product.get("handle"),

            # giá bán
            "price":
                float(
                    variant.get("price", 0)
                ),

            # giá cũ
            "compare_at_price":
                float(
                    variant.get(
                        "compare_at_price",
                        0
                    )
                ),

            # còn hàng hay không
            "available":
                raw_product.get("available"),

            # ảnh đại diện
            "image_url":
                image_url,

            # mô tả html
            "description":
                raw_product.get(
                    "body_html"
                ),

            # tags
            "tags":
                raw_product.get("tags")
        }
    
    #Parse_db.product_images
    def parse_images(self, raw_product):

        result = []

        images = raw_product.get(
            "images",
            []
        )

        product_id = str(
            raw_product.get("id")
        )

        for image in images:

            result.append({

                "product_id":
                    product_id,

                "image_url":
                    image.get("src")
            })

        return result


    #Parse_db.specifications
    def parse_specs(self, raw_product):

        specs = []

        product_id = str(
            raw_product.get("id")
        )

        html = raw_product.get(
            "body_html",
            ""
        )

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        rows = soup.find_all("tr")

        for row in rows:

            cols = row.find_all("td")

            if len(cols) < 2:
                continue

            name = (
                cols[0]
                .get_text(" ", strip=True)
            )

            value = (
                cols[1]
                .get_text(" ", strip=True)
            )

            specs.append({

                "product_id":
                    product_id,

                "spec_name":
                    name,

                "spec_value":
                    value
            })

        return specs