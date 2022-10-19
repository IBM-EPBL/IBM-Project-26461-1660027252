from flask import Flask,render_template

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