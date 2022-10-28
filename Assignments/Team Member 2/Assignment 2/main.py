from flask import Flask,render_template
import ibm_db
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ntv37394;PWD=i5QfgqIlnGog6H1Y",'','')
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