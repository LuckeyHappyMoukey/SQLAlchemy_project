# interface
import hashlib

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Table, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

app = Flask(__name__)

# engine = create_engine('mysql+mysqlconnectorn://root:@localhost/testforfun', echo=True)
engine = create_engine('mysql+pymysql://root:@localhost/testforfun', echo=True)
session = sessionmaker(engine)
db_session = scoped_session(session)
# get Base
Base = declarative_base()


# 代码建表
class User(Base):
    __table__ = Table('user', Base.metadata, autoload_with=engine)


@app.route('/')
def index():
    return 'UnWelcomeWorld'


@app.route('/index', methods=['POST', 'OPTIONS'])
def notindex():
    return 'Hello World!'


@app.route('/mysql', methods=['GET', 'POST', 'OPTIONS'])
def stillindex():
    if request.method == 'POST':
        request_data = request.get_json()
        user_input_name = request_data.get('username')
        user_input_password = request_data.get('password')

        if user_input_name is None or user_input_password is None:
            return jsonify({'error': 'Missing username or password'}), 400

        print(user_input_name, user_input_password)

        # 使用参数化查询防止 SQL 注入
        select_stmt = text("SELECT * FROM user WHERE nickname = :username")
        result = db_session.execute(select_stmt, {'username': user_input_name}).fetchone()

        if result is None:
            return jsonify({'error': 'User not found'}), 404

        # password字段，第2字段
        stored_password = result[2]
        md5password = hashlib.md5(user_input_password.encode('utf-8')).hexdigest()

        if stored_password == md5password:
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Incorrect password'}), 401

    return "GET or OPTIONS request received"



if __name__ == '__main__':
    app.run(debug=True)
