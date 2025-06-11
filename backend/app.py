from flask import Flask, request, jsonify, send_from_directory, abort
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt

CORS(app)  # 允许跨域访问（前后端分离开发时必须）

# 模拟的用户数据库
users = {
    "admin": bcrypt.hashpw("123456".encode(), bcrypt.gensalt()),
    "test": "password"
}
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username not in users:
        return jsonify({"success": False, "message": "用户不存在"}), 401

    hashed_pw = users[username]
    if not bcrypt.checkpw(password.encode(), hashed_pw):
        return jsonify({"success": False, "message": "密码错误"}), 401

    # 登录成功
    return jsonify({"success": True, "message": f"欢迎 {username}！"})

# 设置上传文件的目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'pdf', 'jpg', 'png', 'jpeg', 'ppt', 'pptx'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 提供静态媒体文件的路由
@app.route('/media/<path:filename>')
def serve_media(filename):
    """提供媒体文件下载/播放"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 提供课程资源列表的API
@app.route('/api/courses/<int:course_id>/resources')
def get_course_resources(course_id):
    """获取课程的所有资源"""
    # 这里调用您的数据库函数获取资源列表
    # 例如：resources = resource_functions.get_course_resources(course_id)
    
    # 示例返回数据
    resources = [
        {
            'id': 1,
            'title': 'Python基础教程 - 变量与数据类型',
            'description': '介绍Python中的基本变量和数据类型',
            'resource_type': 'video',
            'file_path': 'courses/1/videos/lesson1.mp4',
            'file_size': 10240000,
            'duration': 1800,
            'url': '/media/courses/1/videos/lesson1.mp4'  # 生成可访问的URL
        },
        # 更多资源...
    ]
    
    return jsonify(resources)

# 文件上传API
@app.route('/api/courses/<int:course_id>/resources', methods=['POST'])
def upload_resource(course_id):
    """上传课程资源"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # 安全处理文件名
        filename = secure_filename(file.filename)
        
        # 创建课程特定的目录
        course_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'courses', str(course_id))
        os.makedirs(course_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(course_dir, filename)
        file.save(file_path)
        
        # 获取文件大小
        file_size = os.path.getsize(file_path)
        
        # 这里调用您的数据库函数添加资源记录
        # 例如：resource_id = resource_functions.add_course_resource(
        #     course_id, 
        #     request.form.get('title'),
        #     request.form.get('description'),
        #     request.form.get('resource_type'),
        #     f'courses/{course_id}/{filename}',
        #     file_size,
        #     int(request.form.get('duration', 0))
        # )
        
        return jsonify({
            'message': 'Resource uploaded successfully',
            'url': f'/media/courses/{course_id}/{filename}'
        })
    
    return jsonify({'error': 'Invalid file type'}), 400








if __name__ == "__main__":
    app.run(port=8000)
