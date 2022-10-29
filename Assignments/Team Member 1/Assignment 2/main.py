from flask import Flask,render_template
import ibm_db
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hzb72342;PWD=S87han59LvW94Hqy",'','')
    print(conn)
except:
    print(ibm_db.conn_errormsg())
app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Index Page!</p>"
@app.route("/home")
def HomePage():
    return "<p>Home Page!</p>"
@app.route("/about")
def AboutPage():
    return "<p>About Page!</p>"
@app.route("/login")
def LoginPage():
    return render_template("login.html")
@app.route("/signup")
def SignupPage():
    return render_template("signup.html")