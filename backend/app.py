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

# 课程管理
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

# 在线测试
@app.route('/tests', methods=['POST'])
def create_test():
    data = request.get_json()
    course_id = data.get('course_id')
    title = data.get('title')
    description = data.get('description')
    duration = data.get('duration')
    passing_score = data.get('passing_score', 60)
    test_id = test_functions.create_test(course_id, title, description, duration, passing_score)
    return jsonify({'message': '测试创建成功', 'test_id': test_id}), 201

# 作业管理
@app.route('/assignments', methods=['POST'])
def create_assignment():
    data = request.get_json()
    course_id = data.get('course_id')
    title = data.get('title')
    description = data.get('description')
    deadline = data.get('deadline')
    max_score = data.get('max_score', 100)
    assignment_id = assignment_functions.create_assignment(course_id, title, description, deadline, max_score)
    return jsonify({'message': '作业创建成功', 'assignment_id': assignment_id}), 201

# 讨论区
@app.route('/discussions', methods=['POST'])
def create_discussion():
    data = request.get_json()
    course_id = data.get('course_id')
    title = data.get('title')
    content = data.get('content')
    author_id = data.get('author_id')
    discussion_id = discussion_functions.create_discussion(course_id, title, content, author_id)
    return jsonify({'message': '讨论主题创建成功', 'discussion_id': discussion_id}), 201

if __name__ == '__main__':
    app.run(debug=True)