from util.db_connection import get_db_connection

def add_course_resource(course_id, title, description, resource_type, file_path, file_size=None, duration=None):
    """添加课程资源"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO course_resources 
               (course_id, title, description, resource_type, file_path, file_size, duration, created_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (course_id, title, description, resource_type, file_path, file_size, duration)
        )
        conn.commit()
        return cursor.lastrowid

def get_course_resources(course_id):
    """获取课程的所有资源"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM course_resources WHERE course_id = ? ORDER BY created_at",
            (course_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

def get_resource_by_id(resource_id):
    """根据资源ID获取资源信息"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT r.*, c.title as course_title, c.teacher_id 
               FROM course_resources r
               JOIN courses c ON r.course_id = c.id
               WHERE r.id = ?""",
            (resource_id,)
        )
        return dict(cursor.fetchone()) if cursor.rowcount > 0 else None

def update_resource(resource_id, title=None, description=None, file_path=None, file_size=None, duration=None):
    """更新资源信息"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        update_fields = []
        params = []
        
        if title:
            update_fields.append("title = ?")
            params.append(title)
        
        if description:
            update_fields.append("description = ?")
            params.append(description)
        
        if file_path:
            update_fields.append("file_path = ?")
            params.append(file_path)
        
        if file_size is not None:
            update_fields.append("file_size = ?")
            params.append(file_size)
        
        if duration is not None:
            update_fields.append("duration = ?")
            params.append(duration)
        
        if update_fields:
            query = f"UPDATE course_resources SET {', '.join(update_fields)} WHERE id = ?"
            params.append(resource_id)
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        
        return False

def delete_resource(resource_id):
    """删除资源"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM course_resources WHERE id = ?", (resource_id,))
        conn.commit()
        return cursor.rowcount > 0
    