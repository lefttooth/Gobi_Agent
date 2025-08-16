from db import engine
from sqlalchemy import text

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("数据库连接成功！")
    except Exception as e:
        print(f"数据库连接失败: {e}")
