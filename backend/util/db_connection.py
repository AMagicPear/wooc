import sqlite3
import os
from contextlib import contextmanager



# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'course_management.db')

@contextmanager
def get_db_connection():
    """提供数据库连接的上下文管理器，确保连接正确关闭"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 返回字典形式的结果
    conn.execute("PRAGMA foreign_keys = ON")  # 启用外键约束
    
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """初始化数据库，创建所有表"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 读取并执行schema.sql中的SQL语句
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema = f.read()
            cursor.executescript(schema)
        conn.commit()
        print("数据库初始化完成")
    