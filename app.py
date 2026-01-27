from flask import Flask, jsonify
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

@app.route('/tables')
def get_tables():
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    return jsonify(tables)

@app.route('/query/<table_name>')
def get_table_data(table_name):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table_name}")
    # cursor.execute(f"SELECT uuid, Challenge_Name, Category, Difficulty, Points, Attempts_Successful, Attempts_Fail FROM {table_name} ORDER BY Category, points;")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
