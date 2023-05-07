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
def index():
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
    db_conn.ping(reconnect=True)
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM employee')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('emp-mgr.html', rows=rows)

@app.route("/payroll", methods=['GET'])
def payroll():
    db_conn.ping(reconnect=True)
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM payroll')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('payroll.html', rows=rows)

@app.route("/attendance", methods=['GET'])
def attendance():
    db_conn.ping(reconnect=True)
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM attendance')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('attendance.html', rows=rows)

@app.route("/leave", methods=['GET'])
def leave():
    db_conn.ping(reconnect=True)
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

@app.route("/addEmpProcess", methods=['GET', 'POST'])
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
    db_conn.ping(reconnect=True)
    cursor = db_conn.cursor()

    cursor.execute(insert_sql, (emp_id, emp_name, gender, dob, address, email, phone_num, job_title, pay_scale, hire_date))
    db_conn.commit()
    cursor.close()

    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM employee')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('emp-mgr.html', rows=rows)

@app.route("/searchEmp", methods=['GET', 'POST'])
def searchEmp():
    return render_template('searchEmp.html')

@app.route("/searchEmpProcess", methods=['GET', 'POST'])
def searchEmpProcess():
    emp_id = request.form['employee_id']

    search_sql = "SELECT * FROM employee WHERE Employee_ID=%s"
    db_conn.ping(reconnect=True)
    cursor = db_conn.cursor()

    cursor.execute(search_sql, (emp_id))
    rows = cursor.fetchall()
    cursor.close()  

    return render_template('emp-mgr.html', rows=rows)

@app.route("/removeEmp", methods=['GET', 'POST'])
def removeEmp():
    return render_template('removeEmp.html')

@app.route("/removeEmpProcess", methods=['GET', 'POST'])
def removeEmpProcess():
    emp_id = request.form['employee_id']

    remove_sql = "DELETE FROM employee WHERE Employee_ID = %s"
    db_conn.ping(reconnect=True)
    cursor = db_conn.cursor()

    cursor.execute(remove_sql, emp_id)
    db_conn.commit()
    cursor.close()

    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM employee')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('emp-mgr.html', rows=rows)
    

#Payroll Manager
@app.route("/payslip")
def payslip():

    return render_template('payEmp.html')

@app.route("/payslipProcess", methods=['GET', 'POST'])
def payslipProcess():
    emp_id = request.form['employee_id']
    salary = request.form['salary']
    date = request.form['date']

    
    cursor = db_conn.cursor()
    insert_sql = "INSERT INTO payroll (Employee_ID, Salary, Date) VALUES (%s, %s, %s)"

    cursor.execute(insert_sql, (emp_id, salary, date))
    db_conn.commit()
    cursor.close()
    db_conn.ping(reconnect=True)
    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM payroll')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('payroll.html', rows=rows)

#Attendance Checker
@app.route("/markAtt")
def markAtt():

    return render_template('markAtt.html')

@app.route("/markAttProcess", methods=['GET', 'POST'])
def markAttProcess():
    emp_id = request.form['employee_id']
    status = request.form['status']
    
    db_conn.ping(reconnect=True)
    cursor = db_conn.cursor()
    #update_sql = "UPDATE attendance SET Status=%s, Time_Stamp=SYSDATE() WHERE Employee_ID=%s"
    insert_sql = "INSERT INTO attendance VALUES (%s,SYSDATE(), %s)"

    cursor.execute(insert_sql, (emp_id, status))
    db_conn.commit()
    cursor.close()

    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM attendance')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('attendance.html', rows=rows)

#Leave Application
@app.route("/leaveApp")
def leaveApp():

    return render_template('leaveApp.html')

@app.route("/leaveAppProcess", methods=['GET', 'POST'])
def leaveAppProcess():
    emp_id = request.form['employee_id']
    date = request.form['leave_date']
    reason = request.form['reason']
    days = request.form['days']

    mc = request.files['mc_evidence']
    db_conn.ping(reconnect=True)
    cursor = db_conn.cursor()
    insert_sql = "INSERT INTO leave_application (Employee_ID, Submission_Date, Reason_of_Leave, Total_Day) VALUES (%s, %s, %s, %s)"

    
    if mc.filename == "":
        return "Please select a file"

    try:
        
        cursor.execute(insert_sql, (emp_id, date, reason, days))
        db_conn.commit()
        # Uplaod image file in S3 #
        mc_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=mc_file_name_in_s3, Body=mc)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                mc_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    cursor = db_conn.cursor()

    cursor.execute('SELECT * FROM leave_application')
    rows = cursor.fetchall()
    cursor.close()

    return render_template('leave.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)