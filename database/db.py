from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Tên SQL Server 
SERVER = "DESKTOP-56H5RB4"

# Database đã tạo sẵn
#DATABASE = "LinhKienMayTinh"
#DATABASE = "TestDb"
DATABASE = "TestDB1"

# Driver thường dùng
DRIVER = "ODBC Driver 17 for SQL Server"

connection_string = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    f"?driver={DRIVER}"
    "&trusted_connection=yes"
)

engine = create_engine(connection_string)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)