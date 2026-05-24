from sqlalchemy import or_

from database.db import SessionLocal
from database.models import Product


class SearchService:

    def search_products(
        self,
        keyword,
        limit=100
    ):

        session = SessionLocal()

        try:

            keyword = keyword.strip()

            return (

                session

                .query(Product)

                .filter(

                    or_(

                        Product.title.ilike(
                            f"%{keyword}%"
                        ),

                        Product.vendor.ilike(
                            f"%{keyword}%"
                        ),

                        Product.product_type.ilike(
                            f"%{keyword}%"
                        ),

                        Product.tags.ilike(
                            f"%{keyword}%"
                        )

                    )

                )

                .order_by(
                    Product.id.desc()
                )

                .limit(limit)

                .all()

            )

        finally:

            session.close()