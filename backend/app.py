from flask import Flask, request, jsonify, send_from_directory, abort,send_file
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
import bcrypt
import util.course_functions as course_functions
import util.resource_functions as resource_functions
import util.enrollment_functions as enrollment_functions
import util.user_functions as user_functions
import util.progress_functions as progress_functions
import util.test_functions as test_functions
import util.assignment_functions as assignment_functions
import util.discussion_functions as discussion_functions

app = Flask(__name__)# 用户管理
CORS(app)  # 允许跨域访问（前后端分离开发时必须）
# __________________________________________账号相关_____________________________________________
# 注册
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')
    user_id = user_functions.register_user(username, password, email, role)
    if user_id:
        return jsonify({'message': '注册成功', 'user_id': user_id,'result':True}), 201
    else:
        return jsonify({'message': '用户名或邮箱已存在','result':False}), 400
# 登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = user_functions.login_user(username, password)
    if user:
        return jsonify({'message': '登录成功', 'user': user,'result':True}), 200
    else:
        return jsonify({'message': '登录失败','result':False}), 401

# 手动映射文件扩展名到 MIME 类型
MIME_TYPE_MAPPING = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'pdf': 'application/pdf',
    'txt': 'text/plain',
    'mp4': 'video/mp4',
    'mp3': 'audio/mpeg',
}
# 获取静态文件
@app.route('/get_file/<path:file_path>')
def get_file(file_path):
    if not os.path.exists(file_path):
        abort(404, description="文件不存在")
    # 检查是否是文件
    if not os.path.isfile(file_path):
        abort(400, description="路径不是一个有效的文件")
    # 获取文件扩展名（小写）
    ext = os.path.splitext(file_path)[1].lstrip('.').lower()

    # 根据扩展名获取 MIME 类型，没有匹配时使用默认值
    mimetype = MIME_TYPE_MAPPING.get(ext, 'application/octet-stream')

    return send_file(file_path, mimetype=mimetype)

# ___________________________________________课程管理_______________________________________________
# 创建课程
@app.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    teacher_id = data.get('teacher_id')
    cover_image = data.get('cover_image')
    course_id = course_functions.create_course(title, description, teacher_id, cover_image)
    return jsonify({'message': '课程创建成功', 'course_id': course_id}), 201
# 获取所有课程
@app.route('/courses', methods=['GET'])
def get_all_courses():
    courses = course_functions.get_all_courses()
    return jsonify({'course':courses}), 200
# 根据课程id获取课程
@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = course_functions.get_course_by_id(course_id)
    if course:
        return jsonify({'course':course,'result':True}), 200
    else:
        return jsonify({'message': '课程不存在','result':False}), 404
# 获取学生选择的所有课程
@app.route('/students/<int:student_id>/courses', methods=['GET'])
def get_student_courses_route(student_id):
    """通过学生ID获取学生已选的所有课程"""
    courses = course_functions.get_student_courses(student_id)
    return jsonify({'courses':courses})
# 获取教师创建的所有课程
@app.route('/teachers/<int:teacher_id>/courses', methods=['GET'])
def get_teacher_courses_route(teacher_id):
    """通过教师ID获取教师创建的所有课程"""
    courses = course_functions.get_teacher_courses(teacher_id)
    return jsonify({'courses':courses})

# 课程资源管理
@app.route('/courses/<int:course_id>/resources', methods=['POST'])
def add_course_resource(course_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    resource_type = data.get('resource_type')
    file_path = data.get('file_path')
    file_size = data.get('file_size')
    duration = data.get('duration')
    resource_id = resource_functions.add_course_resource(course_id, title, description, resource_type, file_path, file_size, duration)
    return jsonify({'message': '资源添加成功', 'resource_id': resource_id}), 201

@app.route('/courses/<int:course_id>/resources', methods=['GET'])
def get_course_resources(course_id):
    resources = resource_functions.get_course_resources(course_id)
    return jsonify({'resources':resources}), 200

# 学生选课
@app.route('/enroll', methods=['POST'])
def enroll_student():
    data = request.get_json()
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    enrollment_id = enrollment_functions.enroll_student(student_id, course_id)
    if enrollment_id:
        return jsonify({'message': '选课成功', 'enrollment_id': enrollment_id ,'result':True}), 201
    else:
        return jsonify({'message': '学生已经选过该课程','result':False}), 400

# 学习进度跟踪
@app.route('/progress', methods=['POST'])
def update_learning_progress():
    data = request.get_json()
    student_id = data.get('student_id')
    resource_id = data.get('resource_id')
    watched_duration = data.get('watched_duration')
    completed = data.get('completed', False)
    success = progress_functions.update_learning_progress(student_id, resource_id, watched_duration, completed)
    if success:
        return jsonify({'message': '学习进度更新成功','result':True}), 200
    else:
        return jsonify({'message': '学习进度更新失败','result':False}), 400

# ____________________________________在线测试____________________________________
# 创建测试
@app.route('/tests', methods=['POST'])
def create_test():
    data = request.get_json()
    course_id = data.get('course_id')
    title = data.get('title')
    description = data.get('description')
    duration = data.get('duration')
    passing_score = data.get('passing_score', 60)

    if not all([course_id, title, description, duration]):
        return jsonify({'message': '缺少必要参数', 'result': False}), 400

    try:
        test_id = test_functions.create_test(course_id, title, description, duration, passing_score)
        return jsonify({
            'message': '测试创建成功',
            'test_id': test_id,
            'result': True
        }), 201
    except Exception as e:
        return jsonify({'message': f'创建失败: {str(e)}', 'result': False}), 500

# 根据测试ID获取测试信息
# @app.route('/tests/<int:test_id>', methods=['GET'])
# def get_test_by_id(test_id):
#     try:
#         test = test_functions.get_test_by_id(test_id)
#         if not test:
#             return jsonify({'message': '测试不存在', 'result': False}), 404
#         return jsonify({
#             'message': '获取成功',
#             'test': test,
#             'result': True
#         }), 200
#     except Exception as e:
#         return jsonify({'message': f'获取失败: {str(e)}', 'result': False}), 500

# 获取课程的所有测试
@app.route('/courses/<int:course_id>/tests', methods=['GET'])
def get_course_tests(course_id):
    try:
        tests = test_functions.get_course_tests(course_id)
        return jsonify({
            'message': '获取成功',
            'tests': tests,
            'result': True
        }), 200
    except Exception as e:
        return jsonify({'message': f'获取失败: {str(e)}', 'result': False}), 500

# 根据测试ID删除测试
@app.route('/tests/<int:test_id>', methods=['DELETE'])
def delete_test_by_id(test_id):
    try:
        success = test_functions.delete_test_by_id(test_id)
        if success:
            return jsonify({'message': '测试删除成功', 'result': True}), 200
        else:
            return jsonify({'message': '测试不存在', 'result': False}), 404
    except Exception as e:
        return jsonify({'message': f'删除失败: {str(e)}', 'result': False}), 500
# 获取所有测试题目的路由
@app.route('/tests/<int:test_id>/questions', methods=['GET'])
def get_test_questions(test_id):
    """获取测试的所有题目"""
    try:
        questions = test_functions.get_test_questions(test_id)
        if not questions:
            return jsonify({'message': '测试题目不存在', 'result': False}), 404
        return jsonify({
            'message': '获取成功',
            'questions': questions,
            'result': True
        }), 200
    except Exception as e:
        return jsonify({'message': f'获取失败: {str(e)}', 'result': False}), 500
# 添加测试题目的路由
@app.route('/tests/<int:test_id>/questions', methods=['POST'])
def add_test_question(test_id):
    """添加测试题目"""
    data = request.get_json()
    question_text = data.get('question_text')
    question_type = data.get('question_type')
    options = data.get('options')  # 仅对选择题有效
    correct_answer = data.get('correct_answer')
    if not all([question_text, question_type, correct_answer]):
        return jsonify({'message': '缺少必要参数', 'result': False}), 400
    try:
        question_id = test_functions.add_test_question(test_id, question_text, question_type, options, correct_answer)
        return jsonify({
            'message': '测试题目添加成功',
            'question_id': question_id,
            'result': True
        }), 201
    except Exception as e:
        return jsonify({'message': f'添加测试题目失败: {str(e)}', 'result': False}), 500


# 开始测试的路由
@app.route('/tests/<int:test_id>/start_test', methods=['POST'])
def api_start_test(test_id):
    data = request.get_json()
    student_id = data.get('student_id')

    if not all([test_id, student_id]):
        return jsonify({'message': '缺少必要参数', 'result': False}), 400

    try:
        attempt_id = test_functions.start_test(test_id, student_id)
        return jsonify({
            'message': '测试开始成功',
            'attempt_id': attempt_id,
            'result': True
        }), 201
    except Exception as e:
        return jsonify({'message': f'开始测试失败: {str(e)}', 'result': False}), 500
    

# 提交测试答案的路由
@app.route('/tests/submit_test_answer', methods=['POST'])
def api_submit_test_answer():
    data = request.get_json()
    attempt_id = data.get('attempt_id')
    question_id = data.get('question_id')
    answer_text = data.get('answer_text')

    if not all([attempt_id, question_id, answer_text]):
        return jsonify({'message': '缺少必要参数', 'result': False}), 400

    try:
        answer_id = test_functions.submit_test_answer(attempt_id, question_id, answer_text)
        if answer_id is None:
            return jsonify({'message': '题目不存在', 'result': False}), 404
        return jsonify({
            'message': '答案提交成功',
            'answer_id': answer_id,
            'result': True
        }), 201
    except Exception as e:
        return jsonify({'message': f'提交答案失败: {str(e)}', 'result': False}), 500

# 完成测试的路由
@app.route('/tests/complete_test', methods=['POST'])
def api_complete_test():
    data = request.get_json()
    attempt_id = data.get('attempt_id')

    if not attempt_id:
        return jsonify({'message': '缺少必要参数', 'result': False}), 400

    try:
        success = test_functions.complete_test(attempt_id)
        if success:
            return jsonify({'message': '测试完成成功', 'result': True}), 200
        else:
            return jsonify({'message': '测试完成失败', 'result': False}), 500
    except Exception as e:
        return jsonify({'message': f'完成测试失败: {str(e)}', 'result': False}), 500



# ____________________________________作业管理______________________________________
# 创建作业
@app.route('/courses/<int:course_id>/assignments', methods=['POST'])
def create_assignment(course_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    deadline = data.get('deadline')
    max_score = data.get('max_score', 100)
    assignment_id = assignment_functions.create_assignment(course_id, title, description, deadline, max_score)
    return jsonify({'message': '作业创建成功', 'assignment_id': assignment_id}), 201

# 获取课程的所有作业
@app.route('/courses/<int:course_id>/assignments', methods=['GET'])
def get_course_assignments(course_id):
    try:
        assignments = assignment_functions.get_course_assignments(course_id)
        return jsonify({
            'message': '获取成功',
            'assignments': assignments,
            'result': True
        }), 200
    except Exception as e:
        return jsonify({'message': f'获取失败: {str(e)}', 'result': False}), 500

#提交作业
@app.route('/assignments/<int:assignment_id>/submit', methods=['POST'])
def submit_assignment(assignment_id):
    data = request.get_json()
    student_id = data.get('student_id')
    content = data.get('content')
    file_path = data.get('file_path')  # 可选参数
    if not all([student_id, content]):
        return jsonify({'message': '缺少必要参数', 'result': False}), 400
    try:
        submission_id = assignment_functions.submit_assignment(assignment_id, student_id, content, file_path)
        return jsonify({
            'message': '作业提交成功',
            'submission_id': submission_id,
            'result': True
        }), 201
    except Exception as e:
        return jsonify({'message': f'提交作业失败: {str(e)}', 'result': False}), 500
    
# 获取学生的作业提交
# @app.route('/assignments/<int:assignment_id>/submissions/<int:student_id>', methods=['GET'])
# def get_student_assignment_submission(assignment_id, student_id):
#     """获取学生的作业提交"""
#     try:
#         submission = assignment_functions.get_student_assignment_submission(assignment_id, student_id)
#         if not submission:
#             return jsonify({'message': '作业提交不存在', 'result': False}), 404
#         return jsonify({
#             'message': '获取成功',
#             'submission': submission,
#             'result': True
#         }), 200
#     except Exception as e:
#         return jsonify({'message': f'获取失败: {str(e)}', 'result': False}), 500

# 获取所有的作业提交
@app.route('/assignments/<int:assignment_id>/submit', methods=['GET'])
def get_all_assignment_submissions(assignment_id):
    """获取作业的所有提交"""
    try:
        submissions = assignment_functions.get_assignment_submissions(assignment_id)
        return jsonify({
            'message': '获取成功',
            'submissions': submissions,
            'result': True
        }), 200
    except Exception as e:
        return jsonify({'message': f'获取失败: {str(e)}', 'result': False}), 500

# 批改作业
@app.route('/assignments/submit/<int:submission_id>/grade', methods=['POST'])
def grade_assignment(submission_id):
    data = request.get_json()
    score = data.get('score')
    feedback = data.get('feedback')
    grader_id = data.get('grader_id')
    if not all([score, feedback, grader_id]):
        return jsonify({'message': '缺少必要参数', 'result': False}), 400
    try:
        success = assignment_functions.grade_assignment(submission_id, score, feedback, grader_id)
        if success:
            return jsonify({'message': '作业批改成功', 'result': True}), 200
        else:
            return jsonify({'message': '作业批改失败', 'result': False}), 500
    except Exception as e:
        return jsonify({'message': f'批改作业失败: {str(e)}', 'result': False}), 500


#获取作业的所有批改
@app.route('/assignments/submit/<int:assignment_id>/grade', methods=['GET'])
def get_assignment_grades(assignment_id):
    """获取作业的所有批改"""
    try:
        grades = assignment_functions.get_assignment_grades(assignment_id)
        return jsonify({
            'message': '获取成功',
            'grades': grades,
            'result': True
        }), 200
    except Exception as e:
        return jsonify({'message': f'获取失败: {str(e)}', 'result': False}), 500




#______________________________________讨论区________________________________________

@app.route('/courses/<int:course_id>/discussions', methods=['POST'])
def create_discussion(course_id):
    """创建讨论主题"""
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    author_id = data.get('author_id')
    
    if not all([course_id, title, content, author_id]):
        return jsonify({'message': '缺少必要参数','result':False}), 400
    
    try:
        discussion_id = discussion_functions.create_discussion(course_id, title, content, author_id)
        return jsonify({
            'message': '讨论主题创建成功', 
            'discussion_id': discussion_id,
            'result': True
        }), 201
    except Exception as e:
        return jsonify({'message': f'创建失败: {str(e)}','result':False}), 500

@app.route('/courses/<int:course_id>/discussions', methods=['GET'])
def get_course_discussions(course_id):
    """获取课程的所有讨论主题"""
    try:
        discussions = discussion_functions.get_course_discussions(course_id)
        return jsonify({
            'message': '获取成功',
            'discussions': discussions,
            'result': True
        }), 200
    except Exception as e:
        return jsonify({'message': f'获取失败: {str(e)}','result':False}), 500

@app.route('/discussions/<int:discussion_id>', methods=['GET'])
def get_discussion_by_id(discussion_id):
    """根据讨论ID获取讨论信息"""
    try:
        discussion = discussion_functions.get_discussion_by_id(discussion_id)
        if not discussion:
            return jsonify({'message': '讨论不存在','result':False}), 404
        return jsonify({
            'message': '获取成功',
            'discussion': discussion,
            'result':True
        }), 200
    except Exception as e:
        return jsonify({'message': f'获取失败: {str(e)}','result':False}), 500

@app.route('/discussions/<int:discussion_id>/replies', methods=['POST'])
def add_discussion_reply(discussion_id):
    """添加讨论回复"""
    data = request.get_json()
    content = data.get('content')
    author_id = data.get('author_id')
    
    if not all([content, author_id]):
        return jsonify({'message': '缺少必要参数','result':False}), 400
    
    try:
        # 检查讨论是否存在
        discussion = discussion_functions.get_discussion_by_id(discussion_id)
        if not discussion:
            return jsonify({'message': '讨论不存在','result':False}), 404
            
        reply_id = discussion_functions.add_discussion_reply(discussion_id, content, author_id)
        return jsonify({
            'message': '回复添加成功', 
            'reply_id': reply_id,
            'result':True
        }), 201
    except Exception as e:
        return jsonify({'message': f'添加失败: {str(e)}','result':False}), 500

@app.route('/discussions/<int:discussion_id>/replies', methods=['GET'])
def get_discussion_replies(discussion_id):
    """获取讨论的所有回复"""
    try:
        # 检查讨论是否存在
        discussion = discussion_functions.get_discussion_by_id(discussion_id)
        if not discussion:
            return jsonify({'message': '讨论不存在','result':False}), 404
            
        replies = discussion_functions.get_discussion_replies(discussion_id)
        return jsonify({
            'message': '获取成功',
            'replies': replies,
            'result':True
        }), 200
    except Exception as e:
        return jsonify({'message': f'获取失败: {str(e)}','result':False}), 500

@app.route('/discussions/<int:discussion_id>', methods=['DELETE'])
def delete_discussion_by_id(discussion_id):
    """根据讨论ID删除讨论主题"""
    try:
        success = discussion_functions.delete_discussion_by_id(discussion_id)
        if success:
            return jsonify({'message': '讨论删除成功','result':True}), 200
        else:
            return jsonify({'message': '讨论不存在','result':False}), 404
    except Exception as e:
        return jsonify({'message': f'删除失败: {str(e)}','result':False}), 500

@app.route('/discussion_replies/<int:reply_id>', methods=['DELETE'])
def delete_discussion_reply_by_id(reply_id):
    """根据回复ID删除讨论回复"""
    try:
        success = discussion_functions.delete_discussion_reply_by_id(reply_id)
        if success:
            return jsonify({'message': '回复删除成功','result':True}), 200
        else:
            return jsonify({'message': '回复不存在','result':False}), 404
    except Exception as e:
        return jsonify({'message': f'删除失败: {str(e)}','result':False}), 500




if __name__ == '__main__':
    app.run(debug=True)