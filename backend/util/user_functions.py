from util.db_connection import get_db_connection
import hashlib
import uuid

def register_user(username, password, email, role):
    """注册新用户"""
    # 密码加密
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email, role, created_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (username, hashed_password, email, role)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # 用户名或邮箱已存在

def login_user(username, password):
    """用户登录验证"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user:
            # 验证密码
            stored_password = user['password']
            # 实际应用中需要从数据库中获取盐值
            salt = stored_password[:32]  # 假设盐值是前32个字符
            hashed_input = hashlib.sha512((password + salt).encode()).hexdigest()
            
            if hashed_input == stored_password:
                return {
                    'id': user['id'],
                    'role': user['role']
                }
        
        return None

def get_user_by_id(user_id):
    """根据用户ID获取用户信息"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, role, created_at FROM users WHERE id = ?", (user_id,))
        return dict(cursor.fetchone()) if cursor.rowcount > 0 else None

def update_user(user_id, username=None, email=None, password=None):
    """更新用户信息"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        update_fields = []
        params = []
        
        if username:
            update_fields.append("username = ?")
            params.append(username)
        
        if email:
            update_fields.append("email = ?")
            params.append(email)
        
        if password:
            # 更新密码需要重新生成盐值和哈希
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
            update_fields.append("password = ?")
            params.append(hashed_password)
        
        if update_fields:
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            params.append(user_id)
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        
        return False
    