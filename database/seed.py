from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

import time

from sqlalchemy import func

from database.db import SessionLocal
from database.db import engine

#Import các Model
from database.models import Base
from database.models import Product
from database.models import ProductImage
from database.models import ProductSpec

from crawlers.gearvn.crawler import GearVNCrawler
from crawlers.gearvn.parser import GearVNParser
from crawlers.gearvn.categories import GEARVN_APIS



from database.models import (
    CpuBenchmark,
    GpuBenchmark
)

from crawlers.benchmark.cpu_scraper import (
    CPUScraper
)

from crawlers.benchmark.gpu_scraper import (
    GPUScraper
)


def to_float(value):

    if value in [None, "", "NA"]:
        return None

    try:

        return float(
            str(value)
            .replace(",", "")
            .replace("$", "")
        )

    except:

        return None


def to_int(value):

    if value in [None, "", "NA"]:
        return None

    try:

        return int(
            float(
                str(value)
                .replace(",", "")
            )
        )

    except:

        return None

def crawl_category(category):
    """
    Crawl toàn bộ sản phẩm của 1 category
    Chạy trong thread riêng
    """

    crawler = GearVNCrawler()

    products = crawler.get_products(
        category
    )

    return category, products


def seed_all_products():

    start_time = time.time()

    print("=" * 70)
    print("KHỞI ĐỘNG IMPORT DỮ LIỆU GEARVN")
    print("=" * 70)

    # ==================================================
    # Tự tạo bảng nếu chưa tồn tại
    # ==================================================

    print("\nKiểm tra database...")

    Base.metadata.create_all(engine)

    print("Database sẵn sàng")

    session = SessionLocal()

    try:

        parser = GearVNParser()

        # ==================================================
        # Lấy toàn bộ product_id hiện có
        # Tránh query SQL hàng nghìn lần
        # ==================================================

        print("\nĐọc danh sách sản phẩm hiện có...")

        existing_ids = {
            x[0]
            for x in session.query(
                Product.product_id
            ).all()
        }

        print(
            f"Đã tìm thấy {len(existing_ids)} sản phẩm trong database"
        )

        # ==================================================
        # Crawl đa luồng
        # ==================================================

        print("\nBắt đầu crawl dữ liệu...\n")

        all_products = {}

        with ThreadPoolExecutor(
            max_workers=8
        ) as executor:

            futures = []

            for category in GEARVN_APIS:

                futures.append(

                    executor.submit(
                        crawl_category,
                        category
                    )

                )

            for future in as_completed(
                futures
            ):

                category, products = (
                    future.result()
                )

                all_products[
                    category
                ] = products

                print(
                    f"✓ Hoàn thành {category}"
                    f" ({len(products)} sản phẩm)"
                )

        # ==================================================
        # Import SQL
        # ==================================================

        total_crawled = 0
        total_inserted = 0
        total_skipped = 0

        print("\n")
        print("=" * 70)
        print("BẮT ĐẦU IMPORT DATABASE")
        print("=" * 70)

        for category, products in all_products.items():

            print()
            print("-" * 60)

            print(
                f"Category: {category}"
            )

            total_crawled += len(products)

            inserted_in_category = 0
            skipped_in_category = 0

            for raw_product in products:

                data = parser.parse_product(
                    raw_product
                )

                product_id = data[
                    "product_id"
                ]

                # ==================================================
                # Đã tồn tại
                # ==================================================

                if product_id in existing_ids:

                    skipped_in_category += 1
                    total_skipped += 1

                    continue

                # ==================================================
                # Thêm mới
                # ==================================================

                product = Product(
                    **data
                )

                session.add(product)
                images = parser.parse_images(
                    raw_product
                )

                for image_data in images:

                    image = ProductImage(
                        **image_data
                    )

                    session.add(image)

                specs = parser.parse_specs(
                    raw_product
                )

                for spec_data in specs:

                    spec = ProductSpec(
                        **spec_data
                    )

                    session.add(spec)

                existing_ids.add(
                    product_id
                )

                inserted_in_category += 1
                total_inserted += 1

            session.commit()

            print(
                f"Tổng crawl: {len(products)}"
            )

            print(
                f"Thêm mới : {inserted_in_category}"
            )

            print(
                f"Bỏ qua   : {skipped_in_category}"
            )

        # ==================================================
        # Tổng kết
        # ==================================================

        total_in_db = (
            session.query(
                func.count(Product.id)
            )
            .scalar()
        )

        elapsed = round(
            time.time() - start_time,
            2
        )

        print()
        print("=" * 70)
        print("KẾT QUẢ CUỐI CÙNG")
        print("=" * 70)

        print(
            f"Tổng sản phẩm crawl : {total_crawled}"
        )

        print(
            f"Tổng thêm mới       : {total_inserted}"
        )

        print(
            f"Tổng bỏ qua         : {total_skipped}"
        )

        print(
            f"Tổng record DB      : {total_in_db}"
        )

        print(
            f"Thời gian chạy      : {elapsed} giây"
        )

    except Exception as e:

        session.rollback()

        print()
        print("=" * 70)
        print("LỖI")
        print("=" * 70)

        print(e)

    finally:

        session.close()

def seed_cpu_benchmarks():

    print()
    print("=" * 70)
    print("IMPORT CPU BENCHMARK")
    print("=" * 70)

    session = SessionLocal()

    try:

        scraper = CPUScraper()

        cpus = scraper.get_all_cpus()

        print(
            f"CPU crawl được: {len(cpus)}"
        )

        existing_ids = {

            str(x[0])

            for x in session.query(
                CpuBenchmark.cpu_id
            ).all()

        }

        # chống trùng trong dataset
        seen_ids = set()

        inserted = 0
        skipped_db = 0
        skipped_duplicate = 0

        for cpu in cpus:

            cpu_id = str(
                cpu.get("id")
            )

            # đã có trong DB
            if cpu_id in existing_ids:

                skipped_db += 1

                continue

            # trùng trong dataset PassMark
            if cpu_id in seen_ids:

                skipped_duplicate += 1

                continue

            seen_ids.add(
                cpu_id
            )

            model = CpuBenchmark(

                cpu_id=cpu_id,

                name=cpu.get("name"),

                cpumark=to_float(
                    cpu.get("cpumark")
                ),

                thread_mark=to_float(
                    cpu.get("thread")
                ),

                cores=to_int(
                    cpu.get("cores")
                ),

                threads=to_int(
                    cpu.get("logicals")
                ),

                tdp=to_float(
                    cpu.get("tdp")
                ),

                speed=to_float(
                    cpu.get("speed")
                ),

                turbo=to_float(
                    cpu.get("turbo")
                ),

                price=to_float(
                    cpu.get("price")
                ),

                samples=to_int(
                    cpu.get("samples")
                ),

                socket=cpu.get(
                    "socket"
                ),

                category=cpu.get(
                    "cat"
                ),

                rank=to_int(
                    cpu.get("rank")
                )

            )

            session.add(model)

            inserted += 1

        session.commit()

        total = (

            session.query(
                func.count(
                    CpuBenchmark.id
                )
            )

            .scalar()

        )

        print()
        print(
            f"CPU thêm mới     : {inserted}"
        )

        print(
            f"CPU đã tồn tại   : {skipped_db}"
        )

        print(
            f"CPU bị trùng API : {skipped_duplicate}"
        )

        print(
            f"Tổng CPU DB      : {total}"
        )

    except Exception as e:

        session.rollback()

        print()
        print("LỖI CPU BENCHMARK")

        print(e)

    finally:

        session.close()

def seed_gpu_benchmarks():

    print()
    print("=" * 70)
    print("IMPORT GPU BENCHMARK")
    print("=" * 70)

    session = SessionLocal()

    try:

        scraper = GPUScraper()

        gpus = scraper.get_all_gpus()

        existing_ids = {

            x[0]

            for x in session.query(
                GpuBenchmark.gpu_id
            ).all()

        }

        inserted = 0

        for gpu in gpus:

            gpu_id = str(
                gpu.get("id")
            )

            if gpu_id in existing_ids:
                continue

            model = GpuBenchmark(

                gpu_id=gpu_id,

                name=gpu.get(
                    "name"
                ),

                g3d_mark=to_float(
                    gpu.get("g3d")
                ),

                g2d_mark=to_float(
                    gpu.get("g2d")
                ),

                memory_size=str(
                    gpu.get(
                        "memSize"
                    )
                ),

                core_clock=str(
                    gpu.get(
                        "coreClk"
                    )
                ),

                memory_clock=str(
                    gpu.get(
                        "memClk"
                    )
                ),

                tdp=to_float(
                    gpu.get("tdp")
                ),

                price=to_float(
                    gpu.get("price")
                ),

                samples=to_int(
                    gpu.get("samples")
                ),

                bus=gpu.get("bus"),

                category=gpu.get(
                    "cat"
                ),

                rank=to_int(
                    gpu.get("rank")
                )
            )

            session.add(model)

            inserted += 1

        session.commit()

        total = session.query(
            func.count(
                GpuBenchmark.id
            )
        ).scalar()

        print(
            f"GPU mới: {inserted}"
        )

        print(
            f"Tổng GPU DB: {total}"
        )

    except Exception as e:

        session.rollback()

        print(e)

    finally:

        session.close()


        
if __name__ == "__main__":

    Base.metadata.create_all(
        bind=engine
    )

    seed_all_products()

    seed_cpu_benchmarks()

    seed_gpu_benchmarks()