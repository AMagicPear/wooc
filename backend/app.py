from flask import Flask

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



if __name__ == "__main__":
    app.run(port=8000)
