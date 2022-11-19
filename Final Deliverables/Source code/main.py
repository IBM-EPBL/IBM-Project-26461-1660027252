from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
import http.client
import json
from werkzeug.utils import secure_filename
import math
import os


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


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login')
def login1():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/authenticate',methods=['GET','POST'])
def authenticate():
    global userId;
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        print(email)
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
            return render_template("dashboard.html",msg=email)
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

@app.route('/getnutri',methods=['GET','POST'])
def getnutri():
    if request.method=="POST":
        name=request.form['name']
        print(name)
        conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")

        headers = {
            'X-RapidAPI-Key': "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            'X-RapidAPI-Host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

        conn.request("GET", "/recipes/guessNutrition?title="+name, headers=headers)

        res = conn.getresponse()
        data = res.read()
        r=json.loads(data)
        val=len(r)

        if val == 2:
            return render_template("getnut.html",msg="invalid")
        else:
            calories = r["calories"]["value"]
            fat = r["fat"]["value"]
            protein = r["protein"]["value"]
            carbs = r["carbs"]["value"]
            def add():
                conn = ibm_db.connect(
                    "DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ntv37394;PWD=i5QfgqIlnGog6H1Y",
                    '', '')
                insert_sql = "INSERT INTO historyi VALUES (?, ?, ?, ?, ?)"
                calories1=round(calories,2)
                protein1=round(protein,2)
                fat1 = round(fat, 2)
                carbs1 = round(carbs, 2)
                print(calories1)
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, name)
                ibm_db.bind_param(prep_stmt, 2, calories1)
                ibm_db.bind_param(prep_stmt, 3, protein1)
                ibm_db.bind_param(prep_stmt, 4, fat1)
                ibm_db.bind_param(prep_stmt, 5, carbs1)

                ibm_db.execute(prep_stmt)



            add()
            return render_template('getnut.html',calories=calories,fat=fat,protein=protein,carbs=carbs)
    return render_template('getnut.html')

@app.route('/up')
def up():
    return render_template('up.html')
# UPLOAD_FOLDER = 'C:\\Users\\bestr\\PycharmProjects\\Nutrition Assistant\\static\\images'
# app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      # f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
      print(f.filename)
      # n=f.filename
      # file_extns=n.split(".")
      # q=repr(file_extns[0])
      # w=repr(file_extns[-1])
      # a2 = q.strip("\'")
      # print(q)
      a = f.filename
      b = a[:-1]
      c = b[:-1]
      d = c[:-1]
      e = d[:-1]
      print(e)

      return render_template('getnut.html',msg=e,img=a)


@app.route('/display')
def display():
    history=[]
    sql = "SELECT * FROM historyi"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        # print ("The Name is : ",  dictionary)
        history.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt)
    if history:
        return render_template('display.html',history = history)
