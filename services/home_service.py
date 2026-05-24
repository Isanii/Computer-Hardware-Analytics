from database.db import SessionLocal

from database.models import Product


class HomeService:

    def get_latest_products(
        self,
        limit=8
    ):

        session = SessionLocal()

        try:

            return (

                session

                .query(Product)

                .order_by(
                    Product.id.desc()
                )

                .limit(limit)

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

    def get_total_vendors(
        self
    ):

        session = SessionLocal()

        try:

            return (

                session

                .query(
                    Product.vendor
                )

                .distinct()

                .count()

            )

        finally:

            session.close()