# app.py
from flask import Flask, request, jsonify
from models import db, Student

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/testforfun'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 创建数据库和表
@app.before_first_request
def create_tables():
    db.create_all()

# 添加学生
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(
        name=data['name'],
        gender=data['gender'],
        height=data['height'],
        age=data['age']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201

# 查询所有学生
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = [
        {
            "id": student.id,
            "name": student.name,
            "gender": student.gender,
            "height": student.height,
            "age": student.age
        } for student in students
    ]
    return jsonify(result)

# 查询特定条件的学生
@app.route('/students/query', methods=['GET'])
def query_students():
    height = request.args.get('height', type=int)
    age = request.args.get('age', type=int)
    query = Student.query
    if height:
        query = query.filter(Student.height >= height)
    if age:
        query = query.filter(Student.age <= age)
    students = query.all()
    result = [
        {
            "id": student.id,
            "name": student.name,
            "gender": student.gender,
            "height": student.height,
            "age": student.age
        } for student in students
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)