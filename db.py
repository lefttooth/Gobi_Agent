from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry

# PostgreSQL/PostGIS 连接字符串示例
DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 可在此扩展模型定义
