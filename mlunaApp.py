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

#routes

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/portfolioSammi")
def portfolioSammi():
    return render_template('portfolio-sammi.html')

@app.route("/portfolioWl")
def portfolioWl():
    return render_template('portfolio-wl.html')

@app.route("/portfolioYz")
def portfolioYz():
    return render_template('portfolio-yz.html')

# four different features

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

#database routes

#EMP Manager
@app.route("/addEmp", methods=['GET', 'POST'])
def addEmp():
    return render_template('addEmp.html')

@app.route("/addEmpProcess", methods=['POST'])
def addEmpProcess():
    emp_id = request.form['employee_id']
    emp_name = request.form['name']
    gender = request.form['gender']
    dob = request.form['dob']
    address = request.form['address']
    email = request.form['email']
    phone_num = request.form['phone']
    job_title = request.form['job_title']
    pay_scale = request.form['pay_scale']
    hire_date = request.form['hire_date']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    cursor.execute(insert_sql, (emp_id, emp_name, gender, dob, address, email, phone_num, job_title, pay_scale, hire_date))
    db_conn.commit()
    cursor.close()

    print("Employee ID" + emp_id + "has been successfully added into the database.")

    return render_template('emp-mgr.html')

@app.route("/updateEmp", methods=['GET', 'POST'])
def updateEmp():
    return render_template('updateEmp.html')

@app.route("/updateEmpProcess", methods=['POST'])
def updateEmpProcess():
    emp_id = request.form['employee_id']
    emp_name = request.form['name']
    gender = request.form['gender']
    dob = request.form['dob']
    address = request.form['address']
    email = request.form['email']
    phone_num = request.form['phone']
    job_title = request.form['job_title']
    pay_scale = request.form['pay_scale']
    hire_date = request.form['hire_date']

    update_sql = "UPDATE employee SET Name=%s, Gender=%s, DOB= %s, Address=%s, Email=%s, Phone Number=%s, Job Title=%s, Pay Scale=%d, Hire Date=%s WHERE Employee_ID=%s,"
    cursor = db_conn.cursor()

    cursor.execute(update_sql, (emp_name, gender, dob, address, email, phone_num, job_title, pay_scale, hire_date, emp_id))
    db_conn.commit()
    cursor.close()   

    print("Employee ID" + emp_id + "has been successfully updated in the database.")
    return render_template('emp-mgr.html')

@app.route("/removeEmp", methods=['GET', 'POST'])
def removeEmp():
    return render_template('removeEmp.html')


@app.route("/removeEmpProcess")
def removeEmpProcess():
    emp_id = request.form['employee_id']

    remove_sql = "DELETE FROM employee WHERE Employee_ID = %s"
    cursor = db_conn.cursor()

    cursor.execute(remove_sql, emp_id)
    db_conn.commit()
    cursor.close()   

    print("Employee ID" + emp_id + "has been successfully removed from the database.")
    return render_template('emp-mgr.html')

#Payroll Manager
@app.route("/payslip")
def payslip():

    return render_template('printPayslip.html')

#Attendance Checker
@app.route("/markAtt")
def markAtt():

    return render_template('markAtt.html')

#Leave Application
@app.route("/leaveApp")
def leaveApp():

    return render_template('leaveApp.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)