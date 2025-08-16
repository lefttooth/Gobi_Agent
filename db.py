from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import os
from dotenv import load_dotenv

# 从 .env 文件读取数据库连接字符串
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 可在此扩展模型定义
