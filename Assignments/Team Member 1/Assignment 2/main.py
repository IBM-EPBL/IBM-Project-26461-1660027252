from flask import Flask,render_template
import ibm_db
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mmb94412;PWD=AI2lT6YaPIHya7ek",'','')
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