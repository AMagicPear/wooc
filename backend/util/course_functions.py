from util.db_connection import get_db_connection

def create_course(title, description, teacher_id, cover_image=None):
    """创建新课程"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO courses (title, description, cover_image, teacher_id, created_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
            (title, description, cover_image, teacher_id)
        )
        conn.commit()
        return cursor.lastrowid

def get_course_by_id(course_id):
    """根据课程ID获取课程信息"""
    course = None
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT c.*, u.username as teacher_name 
                FROM courses c 
                JOIN users u ON c.teacher_id = u.id 
                WHERE c.id = ?
            """, (course_id,))
            row = cursor.fetchone()
            course = dict(row) if row else None
        finally:
            cursor.close()
    return course

def get_all_courses():
    """获取所有课程"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.username as teacher_name, COUNT(e.id) as enrollment_count
            FROM courses c
            JOIN users u ON c.teacher_id = u.id
            LEFT JOIN course_enrollments e ON c.id = e.course_id
            GROUP BY c.id
            ORDER BY c.created_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

def get_teacher_courses(teacher_id):
    """获取教师创建的所有课程"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, COUNT(e.id) as enrollment_count
            FROM courses c
            LEFT JOIN course_enrollments e ON c.id = e.course_id
            WHERE c.teacher_id = ?
            GROUP BY c.id
            ORDER BY c.created_at DESC
        """, (teacher_id,))
        return [dict(row) for row in cursor.fetchall()]

def get_student_courses(student_id):
    """获取学生已选的所有课程"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.username as teacher_name, e.enrolled_at, e.progress, e.completed_at
            FROM course_enrollments e
            JOIN courses c ON e.course_id = c.id
            JOIN users u ON c.teacher_id = u.id
            WHERE e.student_id = ?
            ORDER BY e.enrolled_at DESC
        """, (student_id,))
        return [dict(row) for row in cursor.fetchall()]

def update_course(course_id, title=None, description=None, cover_image=None):
    """更新课程信息"""
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
        
        if cover_image:
            update_fields.append("cover_image = ?")
            params.append(cover_image)
        
        if update_fields:
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE courses SET {', '.join(update_fields)} WHERE id = ?"
            params.append(course_id)
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        
        return False

def delete_course(course_id):
    """删除课程"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        conn.commit()
        return cursor.rowcount > 0

def search_courses(query):
    """搜索课程"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.username as teacher_name, COUNT(e.id) as enrollment_count
            FROM courses c
            JOIN users u ON c.teacher_id = u.id
            LEFT JOIN course_enrollments e ON c.id = e.course_id
            WHERE c.title LIKE ? OR c.description LIKE ?
            GROUP BY c.id
            ORDER BY c.created_at DESC
        """, (f'%{query}%', f'%{query}%'))
        return [dict(row) for row in cursor.fetchall()]
    