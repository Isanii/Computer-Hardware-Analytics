from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import Index

class Base(DeclarativeBase):
    pass


class Product(Base):

    __tablename__ = "products"

    # khóa chính trong database
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # id gốc từ GearVN
    product_id = Column(
        String(100),
        unique=True
    )

    sku = Column(String(100))

    title = Column(Unicode(1000))

    vendor = Column(Unicode(200))

    product_type = Column(Unicode(200))

    handle = Column(Unicode(500))

    price = Column(Float)

    compare_at_price = Column(Float)

    available = Column(Boolean)

    image_url = Column(Text)

    description = Column(UnicodeText)

    tags = Column(UnicodeText)


#Product Image
class ProductImage(Base):

    __tablename__ = "product_images"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    product_id = Column(
        String(100),
        nullable=False
    )

    image_url = Column(Text)


#Product Specification
class ProductSpec(Base):

    __tablename__ = "product_specs"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    product_id = Column(
        String(100),
        nullable=False
    )

    spec_name = Column(
        Unicode(500)
    )

    spec_value = Column(
        UnicodeText
    )


Index("idx_product_images_product_id",ProductImage.product_id)
Index("idx_product_specs_product_id",ProductSpec.product_id)

class CpuBenchmark(Base):

    __tablename__ = "cpu_benchmarks"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    cpu_id = Column(
        String(50),
        unique=True
    )

    name = Column(
        Unicode(500)
    )

    cpumark = Column(Float)

    thread_mark = Column(Float)

    cores = Column(Integer)

    threads = Column(Integer)

    tdp = Column(Float)

    speed = Column(Float)

    turbo = Column(Float)

    price = Column(Float)

    samples = Column(Integer)

    socket = Column(
        Unicode(100)
    )

    category = Column(
        Unicode(100)
    )

    rank = Column(Integer)

class GpuBenchmark(Base):

    __tablename__ = "gpu_benchmarks"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    gpu_id = Column(
        String(50),
        unique=True
    )

    name = Column(
        Unicode(500)
    )

    g3d_mark = Column(Float)

    g2d_mark = Column(Float)

    tdp = Column(Float)

    price = Column(Float)

    samples = Column(Integer)

    memory_size = Column(
        Unicode(100)
    )

    bus = Column(
        Unicode(100)
    )

    core_clock = Column(
        Unicode(100)
    )

    memory_clock = Column(
        Unicode(100)
    )

    category = Column(
        Unicode(100)
    )

    rank = Column(Integer)
Index(
    "idx_cpu_rank",
    CpuBenchmark.rank
)

Index(
    "idx_gpu_rank",
    GpuBenchmark.rank
)