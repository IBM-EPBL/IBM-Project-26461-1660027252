from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
import http.client
import json
from werkzeug.utils import secure_filename
import math
import os
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

app = Flask(__name__)

app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ntv37394;PWD=i5QfgqIlnGog6H1Y",'','')

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

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


# @app.route('/')
# def login():
#     return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    global userId;
    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        sql = "SELECT * FROM users1 WHERE username =? and password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            session['user'] = username
            session['id'] = account['EMAIL']
            userId = account['EMAIL']
            session['email'] = account['EMAIL']
            return redirect("dashboard", code=302)
        else:
            return render_template("login.html", msg="incorrect")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        username=session['user']
        return render_template('dashboard.html',msg=username)
    else:
        return render_template('404.html')



# @app.route('/authenticate',methods=['GET','POST'])
# def authenticate():

@app.route('/pagenot')
def pagenot():
    return render_template('404.html')


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
    if 'user' in session:
        username = session['user']
        if request.method == "POST":
            name = request.form['name']
            print(name)
            conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")

            headers = {
                'X-RapidAPI-Key': "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                'X-RapidAPI-Host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
            }

            conn.request("GET", "/recipes/guessNutrition?title=" + name, headers=headers)

            res = conn.getresponse()
            data = res.read()
            r = json.loads(data)
            val = len(r)

            if val == 2:
                return render_template("getnut.html", msg="invalid")
            else:
                calories = r["calories"]["value"]
                fat = r["fat"]["value"]
                protein = r["protein"]["value"]
                carbs = r["carbs"]["value"]

                def add():
                    conn = ibm_db.connect(
                        "DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ntv37394;PWD=i5QfgqIlnGog6H1Y",
                        '', '')
                    insert_sql = "INSERT INTO historyi VALUES (?, ?, ?, ?, ?, ?)"
                    calories1 = round(calories, 2)
                    protein1 = round(protein, 2)
                    fat1 = round(fat, 2)
                    carbs1 = round(carbs, 2)
                    print(calories1)
                    prep_stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(prep_stmt, 1, username)
                    ibm_db.bind_param(prep_stmt, 2, name)
                    ibm_db.bind_param(prep_stmt, 3, calories1)
                    ibm_db.bind_param(prep_stmt, 4, protein1)
                    ibm_db.bind_param(prep_stmt, 5, fat1)
                    ibm_db.bind_param(prep_stmt, 6, carbs1)

                    ibm_db.execute(prep_stmt)


                add()
                return render_template('getnut.html', calories=calories, fat=fat, protein=protein, carbs=carbs)

    return render_template('getnut.html')

@app.route('/up')
def up():
    if 'user' in session:
        username=session['user']
        return render_template('up.html',msg=username)
    else:
        return render_template('404.html')
    #return render_template('up.html')
# UPLOAD_FOLDER = 'C:\\Users\\bestr\\PycharmProjects\\Nutrition Assistant\\static\\images'
# app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      img_filename = secure_filename(f.filename)
      path=os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
      f.save(path)
      session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
      print(f.filename)
      a = f.filename
      b = a[:-1]
      c = b[:-1]
      d = c[:-1]
      e = d[:-1]
      print(e)


      return render_template('getnut.html',msg=e,img=a)


@app.route('/display')
def display():
    if 'user' in session:
        username=session['user']
        history=[]
        sql = "SELECT * FROM historyi where username=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        dictionary = ibm_db.fetch_both(stmt)
        while dictionary != False:
            # print ("The Name is : ",  dictionary)
            history.append(dictionary)
            dictionary = ibm_db.fetch_both(stmt)
        if history:
            return render_template('display.html',history=history,msg=username)
        return render_template('display.html')

        # stmt = ibm_db.prepare(conn, sql)
        # ibm_db.bind_param(stmt, 1, username)
        # ibm_db.execute(stmt)
        # account=ibm_db.fetch_assoc(stmt)
        # name=account["NAME"]
        # calories=account["CALORIES"]
        # proteins=account["PROTEINS"]
        # fats=account["FATS"]
        # carbs=account["CARBS"]
        # return render_template("display.html",name=name,calories=calories,proteins=proteins,fats=fats,carbs=carbs)


def predictConcept(path):
    USER_ID = 'zm7ia8j6i6pj'
    APP_ID = 'nutrition_assistant'
    # Change these to whatever model and image input you want to use
    MODEL_ID = 'general-image-recognition'
    IMAGE_FILE_LOCATION = path
    # This is optional. You can specify a model version or the empty string for the default
    MODEL_VERSION_ID = ''

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + APP_ID),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    with open(IMAGE_FILE_LOCATION, "rb") as f:
        file_bytes = f.read()

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,
            # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]

    print("Predicted concepts:")
    for concept in output.data.concepts:
        print("%s %d" % (concept.name, concept.value))
        return concept.name


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('index.html')