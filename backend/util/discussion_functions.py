from util.db_connection import get_db_connection

def create_discussion(course_id, title, content, author_id):
    """创建讨论主题"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO discussions 
               (course_id, title, content, author_id, created_at, updated_at) 
               VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
            (course_id, title, content, author_id)
        )
        conn.commit()
        return cursor.lastrowid

def get_course_discussions(course_id):
    """获取课程的所有讨论主题"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT d.*, u.username as author_name, 
               (SELECT COUNT(*) FROM discussion_replies r WHERE r.discussion_id = d.id) as reply_count
               FROM discussions d
               JOIN users u ON d.author_id = u.id
               WHERE d.course_id = ?
               ORDER BY d.updated_at DESC""",
            (course_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

def get_discussion_by_id(discussion_id):
    """根据讨论ID获取讨论信息"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT d.*, u.username as author_name, c.title as course_title
               FROM discussions d
               JOIN users u ON d.author_id = u.id
               JOIN courses c ON d.course_id = c.id
               WHERE d.id = ?""",
            (discussion_id,)
        )
        return dict(cursor.fetchone()) if cursor.rowcount > 0 else None

def add_discussion_reply(discussion_id, content, author_id):
    """添加讨论回复"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO discussion_replies 
               (discussion_id, content, author_id, created_at) 
               VALUES (?, ?, ?, CURRENT_TIMESTAMP)""",
            (discussion_id, content, author_id)
        )
        
        # 更新讨论的更新时间
        cursor.execute(
            "UPDATE discussions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (discussion_id,)
        )
        
        conn.commit()
        return cursor.lastrowid

def get_discussion_replies(discussion_id):
    """获取讨论的所有回复"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT r.*, u.username as author_name
               FROM discussion_replies r
               JOIN users u ON r.author_id = u.id
               WHERE r.discussion_id = ?
               ORDER BY r.created_at""",
            (discussion_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    