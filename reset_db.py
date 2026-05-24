from database.db import engine
from database.models import Base


def reset_database():

    print("=" * 60)
    print("XÓA TOÀN BỘ BẢNG")
    print("=" * 60)

    # tự động xóa tất cả bảng khai báo trong models.py
    Base.metadata.drop_all(bind=engine)

    print("Đã xóa toàn bộ bảng")

    print()
    print("=" * 60)
    print("TẠO LẠI TOÀN BỘ BẢNG")
    print("=" * 60)

    # tự động tạo lại
    Base.metadata.create_all(bind=engine)

    print("Đã tạo lại toàn bộ bảng")


if __name__ == "__main__":

    reset_database()