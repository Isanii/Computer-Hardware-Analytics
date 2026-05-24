from database.db import SessionLocal

from database.models import Product
from database.models import ProductImage
from database.models import ProductSpec
from sqlalchemy import and_
from sqlalchemy import or_
class ProductService:

    def get_all_products(self):

        session = SessionLocal()

        try:

            return (
                session
                .query(Product)
                .all()
            )

        finally:

            session.close()


    def get_product_by_id(
        self,
        product_id
    ):

        session = SessionLocal()

        try:

            return (
                session
                .query(Product)
                .filter(
                    Product.product_id
                    == str(product_id)
                )
                .first()
            )

        finally:

            session.close()


    def get_product_images(
        self,
        product_id
    ):

        session = SessionLocal()

        try:

            return (
                session
                .query(ProductImage)
                .filter(
                    ProductImage.product_id
                    == str(product_id)
                )
                .all()
            )

        finally:

            session.close()


    def get_product_specs(
        self,
        product_id
    ):

        session = SessionLocal()

        try:

            return (
                session
                .query(ProductSpec)
                .filter(
                    ProductSpec.product_id
                    == str(product_id)
                )
                .all()
            )

        finally:

            session.close()

    #Phân trang
    def get_products_page(
        self,
        page=1,
        page_size=21
    ):

        session = SessionLocal()

        try:

            offset = (
                page - 1
            ) * page_size

            return (
                session
                .query(Product)
                .order_by(Product.id.desc())
                .offset(offset)
                .limit(page_size)
                .all()
            )

        finally:

            session.close()
    def get_total_products(
        self
    ):

        session = SessionLocal()

        try:

            return (
                session
                .query(Product)
                .count()
            )

        finally:

            session.close()
    
    def get_filtered_products(
        self,
        page=1,
        page_size=21,
        vendor=None,
        product_type=None,
        price_range=None,
        sort=None
    ):

        if page < 1:
            page = 1

        session = SessionLocal()

        try:

            query = (
                session
                .query(Product)
            )

            # hãng

            if vendor:

                query = query.filter(
                    Product.vendor == vendor
                )

            # loại

            if product_type:

                query = query.filter(
                    Product.product_type
                    == product_type
                )

            # giá

            if price_range:

                if price_range == "0-5000000":

                    query = query.filter(
                        Product.price <= 5000000
                    )

                elif price_range == "5000000-10000000":

                    query = query.filter(
                        Product.price > 5000000,
                        Product.price <= 10000000
                    )

                elif price_range == "10000000-20000000":

                    query = query.filter(
                        Product.price > 10000000,
                        Product.price <= 20000000
                    )

                elif price_range == "20000000+":

                    query = query.filter(
                        Product.price > 20000000
                    )

            # sắp xếp

            if sort == "price_asc":

                query = query.order_by(
                    Product.price.asc()
                )

            elif sort == "price_desc":

                query = query.order_by(
                    Product.price.desc()
                )

            else:

                query = query.order_by(
                    Product.id.desc()
                )

            offset = (
                page - 1
            ) * page_size

            return (

                query

                .offset(offset)

                .limit(page_size)

                .all()

            )

        finally:

            session.close()

    #Lấy danh sách hãng
    def get_all_vendors(
        self
    ):

        session = SessionLocal()

        try:

            rows = (

                session

                .query(
                    Product.vendor
                )

                .distinct()

                .all()

            )

            return [

                x[0]

                for x in rows

                if x[0]

            ]

        finally:

            session.close()

    #Lấy danh sách loại sản phẩm
    def get_all_types(
        self
    ):

        session = SessionLocal()

        try:

            rows = (

                session

                .query(
                    Product.product_type
                )

                .distinct()

                .all()

            )

            mapping = {

                "VGA":
                "Card màn hình"
            }

            result = []
            seen = set()

            for row in rows:

                product_type = (
                    row[0] or ""
                ).strip()

                if not product_type:
                    continue

                product_type = mapping.get(
                    product_type,
                    product_type
                )

                key = (
                    product_type.lower()
                )

                if key not in seen:

                    seen.add(key)

                    result.append(
                        product_type
                    )

            return sorted(result)

        finally:

            session.close()

    def get_filtered_count(
        self,
        vendor=None,
        product_type=None,
        price_range=None
    ):

        session = SessionLocal()

        try:

            query = (
                session
                .query(Product)
            )

            if vendor:

                query = query.filter(
                    Product.vendor == vendor
                )

            if product_type:

                query = query.filter(
                    Product.product_type
                    == product_type
                )

            if price_range:

                if price_range == "0-5000000":

                    query = query.filter(
                        Product.price <= 5000000
                    )

                elif price_range == "5000000-10000000":

                    query = query.filter(
                        Product.price > 5000000,
                        Product.price <= 10000000
                    )

                elif price_range == "10000000-20000000":

                    query = query.filter(
                        Product.price > 10000000,
                        Product.price <= 20000000
                    )

                elif price_range == "20000000+":

                    query = query.filter(
                        Product.price > 20000000
                    )

            return query.count()

        finally:

            session.close()

    def get_category_counts(
        self
    ):

        session = SessionLocal()

        try:

            rows = (

                session

                .query(
                    Product.product_type
                )

                .all()

            )

            mapping = {

                "VGA":
                "Card màn hình"

            }

            result = {}

            for row in rows:

                category = (
                    row[0] or ""
                ).strip()

                if not category:
                    continue

                category = mapping.get(
                    category,
                    category
                )

                result[category] = (

                    result.get(
                        category,
                        0
                    )

                    + 1

                )

            return dict(

                sorted(

                    result.items(),

                    key=lambda x: x[1],

                    reverse=True

                )

            )

        finally:

            session.close()
            
    def search_suggestions(
        self,
        keyword,
        limit=10
    ):

        session = SessionLocal()

        try:

            if not keyword:
                return []

            terms = [

                t.strip()

                for t in keyword.split()

                if t.strip()

            ]

            query = session.query(Product)

            for term in terms:

                query = query.filter(

                    Product.title.ilike(
                        f"%{term}%"
                    )

                )

            return (

                query
                .limit(limit)
                .all()

            )

        finally:

            session.close()