from util.db_connection import get_db_connection

def update_learning_progress(student_id, resource_id, watched_duration, completed=False):
    """更新学习进度"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 检查是否已有记录
        cursor.execute(
            "SELECT id FROM learning_progress WHERE student_id = ? AND resource_id = ?",
            (student_id, resource_id)
        )
        record = cursor.fetchone()
        
        if record:
            # 更新现有记录
            cursor.execute(
                """UPDATE learning_progress 
                   SET watched_duration = ?, completed = ?, last_accessed_at = CURRENT_TIMESTAMP 
                   WHERE id = ?""",
                (watched_duration, completed, record['id'])
            )
        else:
            # 创建新记录
            cursor.execute(
                """INSERT INTO learning_progress 
                   (student_id, resource_id, watched_duration, completed, last_accessed_at) 
                   VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)""",
                (student_id, resource_id, watched_duration, completed)
            )
        
        conn.commit()
        
        # 更新课程整体进度
        update_course_overall_progress(student_id, resource_id)
        
        return cursor.rowcount > 0

def get_resource_progress(student_id, resource_id):
    """获取资源的学习进度"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM learning_progress 
               WHERE student_id = ? AND resource_id = ?""",
            (student_id, resource_id)
        )
        return dict(cursor.fetchone()) if cursor.rowcount > 0 else None

def get_course_progress(student_id, course_id):
    """获取课程的学习进度统计"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT 
                COUNT(r.id) as total_resources,
                SUM(CASE WHEN p.completed = 1 THEN 1 ELSE 0 END) as completed_resources,
                SUM(p.watched_duration) as total_watched_duration
               FROM course_resources r
               LEFT JOIN learning_progress p ON r.id = p.resource_id AND p.student_id = ?
               WHERE r.course_id = ?""",
            (student_id, course_id)
        )
        result = dict(cursor.fetchone())
        
        # 计算完成百分比
        if result['total_resources'] > 0:
            result['completion_percentage'] = (result['completed_resources'] / result['total_resources']) * 100
        else:
            result['completion_percentage'] = 0
            
        return result

def update_course_overall_progress(student_id, resource_id):
    """更新课程整体进度"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 获取资源所属课程
        cursor.execute(
            "SELECT course_id FROM course_resources WHERE id = ?",
            (resource_id,)
        )
        course_result = cursor.fetchone()
        if not course_result:
            return False
        
        course_id = course_result['course_id']
        
        # 计算课程进度
        progress = get_course_progress(student_id, course_id)
        
        # 更新课程进度
        cursor.execute(
            """UPDATE course_enrollments 
               SET progress = ? 
               WHERE student_id = ? AND course_id = ?""",
            (progress['completion_percentage'], student_id, course_id)
        )
        
        conn.commit()
        return cursor.rowcount > 0
    