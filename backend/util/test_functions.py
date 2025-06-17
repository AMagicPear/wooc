from util.db_connection import get_db_connection
import json

def create_test(course_id, title, description, duration, passing_score=60):
    """创建测试"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO tests 
               (course_id, title, description, duration, passing_score, created_at) 
               VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (course_id, title, description, duration, passing_score)
        )
        conn.commit()
        return cursor.lastrowid

def add_test_question(test_id, question_text, question_type, options, correct_answer, score=1):
    """添加测试题目"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 将选项转换为JSON字符串
        options_json = json.dumps(options) if options else None
        
        cursor.execute(
            """INSERT INTO test_questions 
               (test_id, question_text, question_type, options, correct_answer, score) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (test_id, question_text, question_type, options_json, correct_answer, score)
        )
        conn.commit()
        return cursor.lastrowid

def get_course_tests(course_id):
    """获取课程的所有测试"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT t.*, COUNT(q.id) as question_count
               FROM tests t
               LEFT JOIN test_questions q ON t.id = q.test_id
               WHERE t.course_id = ?
               GROUP BY t.id
               ORDER BY t.created_at DESC""",
            (course_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
#有问题
# def get_test_by_id(test_id):
#     """根据测试ID获取测试信息"""
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(
#             """SELECT t.*, c.title as course_title, c.teacher_id
#                FROM tests t
#                JOIN courses c ON t.course_id = c.id
#                WHERE t.id = ?""",
#             (test_id,)
#         )
#         return dict(cursor.fetchone()) if cursor.rowcount > 0 else None

def get_test_questions(test_id):
    """获取测试的所有题目"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT q.*
               FROM test_questions q
               WHERE q.test_id = ?
               ORDER BY q.id""",
            (test_id,)
        )
        questions = []
        for row in cursor.fetchall():
            question = dict(row)
            # 将选项从JSON字符串转换回Python对象
            if question['options']:
                question['options'] = json.loads(question['options'])
            questions.append(question)
        return questions

def start_test(test_id, student_id):
    """开始测试"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO test_attempts 
               (test_id, student_id, started_at) 
               VALUES (?, ?, CURRENT_TIMESTAMP)""",
            (test_id, student_id)
        )
        conn.commit()
        return cursor.lastrowid

def submit_test_answer(attempt_id, question_id, answer_text):
    """提交测试答案"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 获取正确答案
        cursor.execute(
            "SELECT correct_answer, score FROM test_questions WHERE id = ?",
            (question_id,)
        )
        question = cursor.fetchone()
        
        if not question:
            return None
        
        # 判断答案是否正确
        is_correct = answer_text == question['correct_answer']
        score = question['score'] if is_correct else 0
        
        cursor.execute(
            """INSERT INTO test_answers 
               (attempt_id, question_id, answer_text, is_correct, score) 
               VALUES (?, ?, ?, ?, ?)""",
            (attempt_id, question_id, answer_text, is_correct, score)
        )
        conn.commit()
        return cursor.lastrowid

def complete_test(attempt_id):
    """完成测试"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # 计算总分
        cursor.execute(
            """SELECT SUM(score) as total_score
               FROM test_answers
               WHERE attempt_id = ?""",
            (attempt_id,)
        )
        result = cursor.fetchone()
        total_score = result['total_score'] if result['total_score'] else 0
        
        # 更新测试完成状态
        cursor.execute(
            """UPDATE test_attempts 
               SET submitted_at = CURRENT_TIMESTAMP, score = ?
               WHERE id = ?""",
            (total_score, attempt_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def get_student_test_attempt(test_id, student_id):
    """获取学生的测试答卷"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT a.*, t.title as test_title, t.passing_score, t.duration, c.title as course_title
               FROM test_attempts a
               JOIN tests t ON a.test_id = t.id
               JOIN courses c ON t.course_id = c.id
               WHERE a.test_id = ? AND a.student_id = ?
               ORDER BY a.started_at DESC
               LIMIT 1""",
            (test_id, student_id)
        )
        return dict(cursor.fetchone()) if cursor.rowcount > 0 else None

def get_test_attempt_answers(attempt_id):
    """获取测试答卷的所有答案"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT a.*, q.question_text, q.question_type, q.options, q.correct_answer
               FROM test_answers a
               JOIN test_questions q ON a.question_id = q.id
               WHERE a.attempt_id = ?
               ORDER BY q.id""",
            (attempt_id,)
        )
        answers = []
        for row in cursor.fetchall():
            answer = dict(row)
            # 将选项从JSON字符串转换回Python对象
            if answer['options']:
                answer['options'] = json.loads(answer['options'])
            answers.append(answer)
        return answers

def delete_test_by_id(test_id):
    """根据ID删除测试"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tests WHERE id = ?",
            (test_id,)
        )
        conn.commit()
        return cursor.execute("SELECT changes()").fetchone()[0] > 0

def delete_test_question_by_id(question_id):
    """根据ID删除测试题"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM test_questions WHERE id = ?",
            (question_id,)
        )
        conn.commit()
        return cursor.execute("SELECT changes()").fetchone()[0] > 0