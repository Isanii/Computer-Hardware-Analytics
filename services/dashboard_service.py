from database.db import SessionLocal

from database.models import (
    Product,
    CpuBenchmark,
    GpuBenchmark
)

from sqlalchemy import func


class DashboardService:

    def get_statistics(self):

        session = SessionLocal()

        try:

            total_products = (

                session.query(
                    func.count(
                        Product.id
                    )
                )

                .scalar()

            )

            total_cpu = (

                session.query(
                    func.count(
                        CpuBenchmark.id
                    )
                )

                .scalar()

            )

            total_gpu = (

                session.query(
                    func.count(
                        GpuBenchmark.id
                    )
                )

                .scalar()

            )

            total_vendor = (

                session.query(
                    func.count(
                        func.distinct(
                            Product.vendor
                        )
                    )
                )

                .scalar()

            )

            return {

                "products":
                total_products,

                "cpus":
                total_cpu,

                "gpus":
                total_gpu,

                "vendors":
                total_vendor

            }

        finally:

            session.close()

    def get_top_cpu_chart(self):

        session = SessionLocal()

        try:

            cpus = (

                session.query(
                    CpuBenchmark
                )

                .order_by(
                    CpuBenchmark.cpumark.desc()
                )

                .limit(10)

                .all()

            )

            return {

                "labels": [

                    cpu.name

                    for cpu in cpus

                ],

                "values": [

                    cpu.cpumark or 0

                    for cpu in cpus

                ]

            }

        finally:

            session.close()

    def get_top_gpu_chart(self):

        session = SessionLocal()

        try:

            gpus = (

                session.query(
                    GpuBenchmark
                )

                .order_by(
                    GpuBenchmark.g3d_mark.desc()
                )

                .limit(10)

                .all()

            )

            return {

                "labels": [

                    gpu.name

                    for gpu in gpus

                ],

                "values": [

                    gpu.g3d_mark or 0

                    for gpu in gpus

                ]

            }

        finally:

            session.close()


    def get_vendor_chart(self):

        session = SessionLocal()

        try:

            result = (

                session.query(

                    Product.vendor,

                    func.count(
                        Product.id
                    )

                )

                .group_by(
                    Product.vendor
                )

                .order_by(
                    func.count(
                        Product.id
                    ).desc()
                )

                .limit(10)

                .all()

            )

            return {

                "labels": [

                    row[0]

                    for row in result

                ],

                "values": [

                    row[1]

                    for row in result

                ]

            }

        finally:

            session.close()


    def get_product_type_chart(self):

        session = SessionLocal()

        try:

            result = (

                session.query(

                    Product.product_type,

                    func.count(
                        Product.id
                    )

                )

                .group_by(
                    Product.product_type
                )

                .order_by(
                    func.count(
                        Product.id
                    ).desc()
                )

                .limit(10)

                .all()

            )

            return {

                "labels": [

                    row[0] or "Unknown"

                    for row in result

                ],

                "values": [

                    row[1]

                    for row in result

                ]

            }

        finally:

            session.close()

    def get_avg_price_chart(self):

        session = SessionLocal()

        try:

            result = (

                session.query(

                    Product.vendor,

                    func.avg(
                        Product.price
                    )

                )

                .group_by(
                    Product.vendor
                )

                .order_by(
                    func.avg(
                        Product.price
                    ).desc()
                )

                .limit(10)

                .all()

            )

            return {

                "labels": [

                    row[0]

                    for row in result

                ],

                "values": [

                    float(row[1] or 0)

                    for row in result

                ]

            }

        finally:

            session.close()