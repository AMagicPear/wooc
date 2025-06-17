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
        with open('util/schema.sql', 'r', encoding='utf-8') as f:
            schema = f.read()
            cursor.executescript(schema)
        conn.commit()
        print("数据库初始化完成")

def delete_database(db_path):
    """通过重新执行 schema.sql 重置数据库"""
    """重置SQLite数据库，清空所有表并重置自增主键"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. 禁用外键约束
        cursor.execute('PRAGMA foreign_keys = OFF')
        
        # 2. 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        
        # 3. 清空每个表并重置自增主键
        for table in tables:
            if table.startswith('sqlite_'):
                continue  # 跳过系统表
            # 清空表数据
            cursor.execute(f'DELETE FROM {table}')
            # 重置自增主键（通过VACUUM）
            cursor.execute(f'VACUUM {table}')
        # 4. 启用外键约束
        cursor.execute('PRAGMA foreign_keys = ON')
        conn.commit()
        print("数据库重置完成，所有表已清空且自增主键已重置")
        
    except sqlite3.Error as e:
        print(f"重置数据库时出错: {e}")
        conn.rollback()
    finally:
        conn.close()
    