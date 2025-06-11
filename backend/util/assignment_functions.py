from util.db_connection import get_db_connection

def create_assignment(course_id, title, description, deadline, max_score=100):
    """创建作业"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO assignments 
               (course_id, title, description, deadline, max_score, created_at) 
               VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (course_id, title, description, deadline, max_score)
        )
        conn.commit()
        return cursor.lastrowid

def get_course_assignments(course_id):
    """获取课程的所有作业"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM assignments 
               WHERE course_id = ?
               ORDER BY deadline DESC""",
            (course_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

def get_assignment_by_id(assignment_id):
    """根据作业ID获取作业信息"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT a.*, c.title as course_title, c.teacher_id
               FROM assignments a
               JOIN courses c ON a.course_id = c.id
               WHERE a.id = ?""",
            (assignment_id,)
        )
        return dict(cursor.fetchone()) if cursor.rowcount > 0 else None

def submit_assignment(assignment_id, student_id, content=None, file_path=None):
    """提交作业"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO assignment_submissions 
               (assignment_id, student_id, content, file_path, submitted_at) 
               VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (assignment_id, student_id, content, file_path)
        )
        conn.commit()
        return cursor.lastrowid

def get_student_assignment_submission(assignment_id, student_id):
    """获取学生的作业提交"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT s.*, a.title as assignment_title, a.max_score, a.deadline, c.title as course_title
               FROM assignment_submissions s
               JOIN assignments a ON s.assignment_id = a.id
               JOIN courses c ON a.course_id = c.id
               WHERE s.assignment_id = ? AND s.student_id = ?""",
            (assignment_id, student_id)
        )
        return dict(cursor.fetchone()) if cursor.rowcount > 0 else None

def get_assignment_submissions(assignment_id):
    """获取作业的所有提交"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT s.*, u.username, u.email
               FROM assignment_submissions s
               JOIN users u ON s.student_id = u.id
               WHERE s.assignment_id = ?
               ORDER BY s.submitted_at DESC""",
            (assignment_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

def grade_assignment(submission_id, score, feedback, grader_id):
    """批改作业"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE assignment_submissions 
               SET score = ?, feedback = ?, graded_at = CURRENT_TIMESTAMP, grader_id = ?
               WHERE id = ?""",
            (score, feedback, grader_id, submission_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    