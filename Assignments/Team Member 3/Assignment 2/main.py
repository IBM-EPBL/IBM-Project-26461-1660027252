from flask import Flask,render_template
import ibm_db
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=pwy87009;PWD=2gCjFgDWWNEyYPfe",'','')
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