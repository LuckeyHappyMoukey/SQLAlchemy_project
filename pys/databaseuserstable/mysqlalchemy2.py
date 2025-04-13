import hashlib
import json

from flask import Flask, request
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

app = Flask(__name__)

#learn 1
engine = create_engine("mysql+pymysql://root:123456@localhost/testforfun")
session = sessionmaker(engine)
db_session = scoped_session(session)
Base = declarative_base()
#learn 2
# 采用读取表结构 非自己写
class User(Base):
    __table__ = Table('users', Base.metadata, autoload_with=engine)


def reg(request_data):
    # 检查请求数据是否为空
    if request_data is None:
        return "error: request data is missing"
#learn 3
    # 解析JSON数据
    # 这里应该用request.get_json()
    # request_data = json.loads(request_data)
    request_data = request.get_json(request_data)

    # 获取用户名和密码
    username = request_data.get('username')
    password = request_data.get('password')
#learn 4
    nickname = request_data.get('nickname', '')  # 提供默认值以防缺失
    picture = request_data.get('picture', '')  # 提供默认值以防缺失

    # 检查用户名和密码是否为空
    if username is None or password is None:
        return "error: username and password are required"

    # 检查用户名长度（假设用户名长度在3到20个字符之间）
    if len(username) < 3 or len(username) > 20:
        return "error: username must be between 3 and 20 characters"

    # 检查密码长度（假设密码长度至少为6个字符）
    if len(password) < 6:
        return "error: password must be at least 6 characters long"

    # MD5加密 方便测试
    password = hashlib.md5(password.encode('utf-8')).hexdigest()

    insert_data = {
        'username': username,
        'password': password,
        'nickname': nickname,
        'picture': picture,
    }

    try:
        # 创建用户实例
        user = User(**insert_data)
        # 保存到数据库
        db_session.add(user)
        db_session.commit()
        return "success"
    except Exception as e:
        # 如果发生错误，回滚事务并返回错误信息
        db_session.rollback()
        return f"error: {str(e)}"
    finally:
        # 关闭数据库会话
        db_session.close()
@app.route('/', methods=['GET', 'POST'])
def index():
    request_data = request.get_json()
    reg(request_data)
    return "success"

if __name__ == '__main__':
    app.run(debug=True)