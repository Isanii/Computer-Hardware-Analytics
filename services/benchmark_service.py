from database.db import SessionLocal

from database.models import (
    CpuBenchmark,
    GpuBenchmark
)


class BenchmarkService:

    def get_cpu_benchmarks(
        self,
        page=1,
        page_size=50,
        keyword=None
    ):

        session = SessionLocal()

        try:

            query = session.query(
                CpuBenchmark
            )

            if keyword:

                terms = [

                    term.strip()

                    for term in keyword.split()

                    if term.strip()

            ]

                for term in terms:

                    query = query.filter(

                        CpuBenchmark.name.ilike(
                            f"%{term}%"
                        )

                    )

            query = query.order_by(
                CpuBenchmark.rank.asc()
            )

            return (

                query

                .offset(
                    (page - 1)
                    * page_size
                )

                .limit(
                    page_size
                )

                .all()

            )

        finally:

            session.close()

    def get_cpu_count(
        self,
        keyword=None
    ):

        session = SessionLocal()

        try:

            query = session.query(
                CpuBenchmark
            )

            if keyword:

                terms = [

                    term.strip()

                    for term in keyword.split()

                    if term.strip()

                ]

                for term in terms:

                    query = query.filter(

                        CpuBenchmark.name.ilike(
                            f"%{term}%"
                        )

                    )
            return query.count()

        finally:

            session.close()

    def get_gpu_benchmarks(
        self,
        page=1,
        page_size=50,
        keyword=None
    ):

        session = SessionLocal()

        try:

            query = session.query(
                GpuBenchmark
            )

            if keyword:


                terms = [

                    term.strip()

                    for term in keyword.split()

                    if term.strip()

                ]

                for term in terms:

                    query = query.filter(

                        GpuBenchmark.name.ilike(
                            f"%{term}%"
                        )

                    )

            query = query.order_by(
                GpuBenchmark.g3d_mark.desc()
            )

            return (

                query

                .offset(
                    (page - 1)
                    * page_size
                )

                .limit(
                    page_size
                )

                .all()

            )

        finally:

            session.close()

    def get_gpu_count(
        self,
        keyword=None
    ):

        session = SessionLocal()

        try:

            query = session.query(
                GpuBenchmark
            )

            if keyword:

                terms = [

                    term.strip()

                    for term in keyword.split()

                    if term.strip()

                ]

                for term in terms:

                    query = query.filter(

                        GpuBenchmark.name.ilike(
                            f"%{term}%"
                        )

                    )

            return query.count()

        finally:

            session.close()


    def get_cpu_by_id(
        self,
        cpu_id
    ):

        session = SessionLocal()

        try:

            return (

                session

                .query(
                    CpuBenchmark
                )

                .filter(
                    CpuBenchmark.cpu_id == cpu_id
                )

                .first()

            )

        finally:

            session.close()


    def get_top_cpus(
        self,
        limit=100
    ):

        session = SessionLocal()

        try:

            return (

                session.query(
                    CpuBenchmark
                )

                .order_by(
                    CpuBenchmark.cpumark.desc()
                )

                .limit(limit)

                .all()

            )

        finally:

            session.close()

    def get_gpu_by_id(
        self,
        gpu_id
    ):

        session = SessionLocal()

        try:

            return (

                session

                .query(
                    GpuBenchmark
                )

                .filter(
                    GpuBenchmark.gpu_id == gpu_id
                )

                .first()

            )

        finally:

            session.close()


    def get_top_gpus(
        self,
        limit=200
    ):

        session = SessionLocal()

        try:

            return (

                session.query(
                    GpuBenchmark
                )

                .order_by(
                    GpuBenchmark.g3d_mark.desc()
                )

                .limit(limit)

                .all()

            )

        finally:

            session.close()


    def search_cpu(
        self,
        keyword
    ):

        session = SessionLocal()

        try:

            if not keyword:
                return []

            terms = [

                term.strip()

                for term in keyword.split()

                if term.strip()

            ]

            query = session.query(
                CpuBenchmark
            )

            for term in terms:

                query = query.filter(

                    CpuBenchmark.name.ilike(
                        f"%{term}%"
                    )

                )

            return (

                query

                .limit(10)

                .all()

            )

        finally:

            session.close()

    def search_gpu(
        self,
        keyword
    ):

        session = SessionLocal()

        try:

            if not keyword:
                return []

            terms = [

                term.strip()

                for term in keyword.split()

                if term.strip()

            ]

            query = session.query(
                GpuBenchmark
            )

            for term in terms:

                query = query.filter(

                    GpuBenchmark.name.ilike(
                        f"%{term}%"
                    )

                )

            return (

                query

                .limit(10)

                .all()

            )

        finally:

            session.close()

    def get_cpu_list(self):

        session = SessionLocal()

        try:

            return (

                session

                .query(CpuBenchmark)

                .order_by(
                    CpuBenchmark.rank.asc()
                )

                .all()

            )

        finally:

            session.close()


    def get_gpu_list(self):

        session = SessionLocal()

        try:

            return (

                session

                .query(GpuBenchmark)

                .order_by(
                    GpuBenchmark.rank.asc()
                )

                .all()

            )

        finally:

            session.close()