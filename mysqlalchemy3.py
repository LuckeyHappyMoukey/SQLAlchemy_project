# app.py
from flask import Flask, request, jsonify
from models import db, Student

app = Flask(__name__)
# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # 使用 SQLite 作为示例数据库 真的加表写数据有点麻烦
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/students', methods=['POST'])
def query_students():
    if request.method == 'POST':
        request_data = request.get_json()
        if not request_data:
            return jsonify({'error': 'No data provided'}), 400

        # **1. 查询满足大于等于/小于等于的方法（如身高大于160的学生）**
        height_gte = request_data.get('height_gte')
        height_lte = request_data.get('height_lte')
        age_gte = request_data.get('age_gte')
        age_lte = request_data.get('age_lte')

        # **2. 范围查询方法（如身高、年龄等自行定义）**
        height_range = request_data.get('height_range')
        age_range = request_data.get('age_range')

        # **3. 模糊匹配并区分大小写**
        name_like = request_data.get('name_like')
        name_case_sensitive = request_data.get('name_case_sensitive', False)

        # 构建查询
        query = Student.query

        if height_gte is not None:
            query = query.filter(Student.height >= height_gte)

        if height_lte is not None:
            query = query.filter(Student.height <= height_lte)

        if age_gte is not None:
            query = query.filter(Student.age >= age_gte)

        if age_lte is not None:
            query = query.filter(Student.age <= age_lte)

        if height_range is not None and len(height_range) == 2:
            query = query.filter(Student.height >= height_range[0]).filter(Student.height <= height_range[1])

        if age_range is not None and len(age_range) == 2:
            query = query.filter(Student.age >= age_range[0]).filter(Student.age <= age_range[1])

        if name_like is not None:
            if name_case_sensitive:
                query = query.filter(Student.name.like(name_like))
            else:
                query = query.filter(Student.name.ilike(name_like))

        # **执行查询**
        results = query.all()

        # 将结果转换为字典列表
        students = [{'id': student.id, 'name': student.name, 'gender': student.gender, 'height': student.height, 'age': student.age} for student in results]

        return jsonify(students), 200

    return "GET request received"

if __name__ == '__main__':
    app.run(debug=True)
