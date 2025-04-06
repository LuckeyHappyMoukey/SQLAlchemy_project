from flask import Flask,request,jsonify
from sqlalchemy import Table, create_engine, Column, Integer, String, CHAR, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# 创建 Flask 应用
app = Flask[__name__]
###
# 创建数据库引擎
engine = create_engine('mysql+mysqlconnector://root:@localhost/testforfun')
# 创建会话工厂
sessionmaker = sessionmaker(bind=engine)
# 创建会话
db_session = scoped_session(sessionmaker)
# 创建基类
Base = declarative_base()
###

# 代码中定义学生表
class Student(Base):
    # 已存在注释部分
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    gender = Column(CHAR(1), CheckConstraint("gender IN ('M', 'F')"))
    height = Column(Integer)
    age = Column(Integer)
    # 已存在注释部分
    __table__ = Table('students', Base.metadata, autoload_with=engine)

# 创建表
Base.metadata.create_all(engine)

print("学生表 'students' 已成功创建！")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # 查询所有学生信息
        students = db_session.query(Student).all()
        # 格式化输出
        students_list = []
        for student in students:
            students_list.append({'id': student.id, 'name': student.name, 'gender': student.gender, 'height': student.height, 'age': student.age})
        return jsonify(students_list)
    elif request.method == 'POST':
        # 接收前端数据
        data = request.get_json()
        # 插入新学生信息
        new_student = Student(name=data['name'], gender=data['gender'], height=data['height'], age=data['age'])
        db_session.add(new_student)
        db_session.commit()
        return jsonify({'message': '学生信息添加成功！'})
###

