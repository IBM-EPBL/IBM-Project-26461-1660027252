from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)

app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ntv37394;PWD=i5QfgqIlnGog6H1Y",'','')



@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/addrec",methods=['GET','POST'])
def addrec():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        sql = "SELECT * FROM users1 WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            return render_template("signup.html",msg="Already a user")
        else:
            insert_sql = "INSERT INTO users1 VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)

            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'

        return render_template('signup.html', msg=msg)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate',methods=['GET','POST'])
def authenticate():
    global userId;
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']

        sql = "SELECT * FROM users1 WHERE email =? and password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            session['loggedin']=True
            session['id']=account['EMAIL']
            userId=account['EMAIL']
            session['email']=account['EMAIL']
            return render_template("dashboard.html")
        else:
            return render_template("login.html",msg="incorrect")

@app.route("/checkpass",methods=['GET','POST'])
def checkpass():
    msg=''
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        sql = "select * from users1 where email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        if account:
            sql1="update users1 set password=? where email=?"
            stmt = ibm_db.prepare(conn, sql1)
            ibm_db.bind_param(stmt, 1, password)
            ibm_db.bind_param(stmt, 2, email)

            ibm_db.execute(stmt)
            return render_template('forgotpw.html',msg="changed")
        else:
            return render_template('forgotpw.html',msg="incorrect")
@app.route('/forgotpw')
def forgotpw():
    return render_template('forgotpw.html')


