from sqlalchemy import or_

from database.db import SessionLocal
from database.models import Product


class SearchService:

    from sqlalchemy import and_
    from sqlalchemy import or_

    def search_products(
        self,
        keyword,
        limit=10000
    ):

        session = SessionLocal()

        try:

            keyword = keyword.strip()

            terms = [

                term.strip()

                for term in keyword.split()

                if term.strip()

            ]

            query = (
                session.query(Product)
            )

            for term in terms:

                query = query.filter(

                    or_(

                        Product.title.ilike(
                            f"%{term}%"
                        ),

                        Product.vendor.ilike(
                            f"%{term}%"
                        )

                    )

                )

            return (

                query

                .order_by(
                    Product.title.asc()
                )

                .limit(limit)

                .all()

            )
        finally:

            session.close()