from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'testforfun'
}

# Create the table if it doesn't exist
def create_table():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = """
            CREATE TABLE IF NOT EXISTS xxx (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                gender CHAR(1),
                height INT,
                age INT
            )
            """
            cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()

create_table()

# Route to handle POST requests for adding students
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO xxx (name, gender, height, age) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (data['name'], data['gender'], data['height'], data['age']))
        connection.commit()
    finally:
        connection.close()
    return jsonify(data), 201

# Route to handle GET requests for querying all students in the table
@app.route('/xxx', methods=['GET'])
def get_students():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM xxx"
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()
    return jsonify(result), 200

# Route to handle the root path
@app.route('/', methods=['GET'])
def root():
    return "Enter 'xxx' to query the table", 200

if __name__ == '__main__':
    app.run(debug=True)
