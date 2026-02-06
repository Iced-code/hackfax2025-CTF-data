from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
mysql_pass = os.environ.get("MYSQL_PASSWORD")

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=mysql_pass,
    database="ctf_2025"
)

app = Flask(__name__)
CORS(app)

@app.route('/')
def default_route():
    return {"connected_to_database": conn.is_connected()}

@app.route('/tables')
def get_tables():
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    return jsonify(tables)

@app.route('/query/<table_name>')
def get_table_data(table_name):
    query = f"SELECT * FROM {table_name} ORDER BY Category, FIELD(Difficulty, 'Easy', 'Medium', 'Hard');"
    # query = f"SELECT * FROM {table_name} ORDER BY FIELD(Difficulty, 'Easy', 'Medium', 'Hard'), Category;"
    
    """ isAscending = request.args.get("isAscending")
    print(f"{isAscending}\n")

    query_list = list(query)
    if isAscending:
        query_list.insert(-1, " DESC")
    else:
        query_list.insert(-1, " ASC")

    full_query = "".join(query_list)
    print(full_query) """

    cursor = conn.cursor(dictionary=True)
    #cursor.execute(f"SELECT * FROM {table_name}")
    cursor.execute(query)
    # cursor.execute(f"SELECT * FROM {table_name} WHERE Difficulty = 'Easy';SELECT * FROM {table_name} WHERE Difficulty = 'Medium';")

    # cursor.execute(f"SELECT uuid, Challenge_Name, Category, Difficulty, Points, Attempts_Successful, Attempts_Fail FROM {table_name} ORDER BY Category, points;")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
