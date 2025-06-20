from util.db_connection import get_db_connection
import sqlite3

def enroll_student(student_id, course_id):
    """学生选课"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO course_enrollments (student_id, course_id, enrolled_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (student_id, course_id)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # 学生已经选过该课程

def unenroll_student(student_id, course_id):
    """学生退课"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM course_enrollments WHERE student_id = ? AND course_id = ?",
            (student_id, course_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def update_course_progress(student_id, course_id, progress):
    """更新课程进度"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE course_enrollments SET progress = ?, updated_at = CURRENT_TIMESTAMP WHERE student_id = ? AND course_id = ?",
            (progress, student_id, course_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def mark_course_completed(student_id, course_id):
    """标记课程已完成"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE course_enrollments 
               SET progress = 100, completed_at = CURRENT_TIMESTAMP 
               WHERE student_id = ? AND course_id = ?""",
            (student_id, course_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def get_course_enrollments(course_id):
    """获取课程的所有选课学生"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT e.*, u.username, u.email
               FROM course_enrollments e
               JOIN users u ON e.student_id = u.id
               WHERE e.course_id = ?
               ORDER BY e.enrolled_at DESC""",
            (course_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    