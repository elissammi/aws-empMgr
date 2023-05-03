from flask import Flask, render_template, request
from pymysql import connections
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/empMgr", methods=['GET'])
def empMgr():
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM employee')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('emp-mgr.html', rows=rows)

@app.route("/payroll", methods=['GET'])
def payroll():
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM payroll')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('payroll.html', rows=rows)

@app.route("/attendance", methods=['GET'])
def attendance():
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM attendance')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('attendance.html', rows=rows)

@app.route("/leave", methods=['GET'])
def leave():
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM leave_application')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('leave.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)