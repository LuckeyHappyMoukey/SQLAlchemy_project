import pymysql
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'testforfun',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 创建数据库连接
def get_db_connection():
    return pymysql.connect(**db_config)

# 查询指定表格中的数据
@app.route('/<table_name>', methods=['GET', 'POST'])
def query_table(table_name):
    if request.method == 'POST':
        column1 = request.form.get('column1')
        operator1 = request.form.get('operator1')
        value1 = request.form.get('value1')

        column2 = request.form.get('column2')
        operator2 = request.form.get('operator2')
        value2 = request.form.get('value2')

        query = f"SELECT * FROM {table_name}"
        conditions = []
        params = []

        if column1 and operator1 and value1:
            sql_operator1 = convert_operator(operator1)
            if sql_operator1 is None:
                return render_template('table.html', data=[], table_name=table_name, error="无效的操作符1")

            if operator1 == 'like':
                value1 = f"%{value1}%"
            elif operator1 in ['gt', 'lt', 'ge', 'le']:
                try:
                    value1 = float(value1)
                except ValueError:
                    return render_template('table.html', data=[], table_name=table_name, error="值1必须是数字")

            conditions.append(f"{column1} {sql_operator1} %s")
            params.append(value1)

        if column2 and operator2 and value2:
            sql_operator2 = convert_operator(operator2)
            if sql_operator2 is None:
                return render_template('table.html', data=[], table_name=table_name, error="无效的操作符2")

            if operator2 == 'like':
                value2 = f"%{value2}%"
            elif operator2 in ['gt', 'lt', 'ge', 'le']:
                try:
                    value2 = float(value2)
                except ValueError:
                    return render_template('table.html', data=[], table_name=table_name, error="值2必须是数字")

            conditions.append(f"{column2} {sql_operator2} %s")
            params.append(value2)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                data = cursor.fetchall()
        except pymysql.err.ProgrammingError as e:
            return render_template('table.html', data=[], table_name=table_name, error=str(e))
        finally:
            connection.close()

        return render_template('table.html', data=data, table_name=table_name)
    else:
        # 默认查询所有数据
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()
        finally:
            connection.close()
        return render_template('table.html', data=data, table_name=table_name)

def convert_operator(operator):
    operators = {
        'eq': '=',
        'gt': '>',
        'lt': '<',
        'ge': '>=',
        'le': '<=',
        'like': 'LIKE'
    }
    return operators.get(operator)

# 主页，输入表格名并跳转
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        table_name = request.form['table_name']
        return redirect(url_for('query_table', table_name=table_name))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
