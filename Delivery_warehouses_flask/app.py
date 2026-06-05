from flask import Flask, render_template, request, session
from classes.company import Company
from datafile import filename
from classes.order import Order
from classes.vehicle import Vehicle
from classes.warehouse import Warehouse
from classes.userlogin import Userlogin
from subs.apps_company import apps_company
from subs.apps_gform import apps_gform 
from subs.apps_subform import apps_subform 
from subs.apps_userlogin import apps_userlogin
from subs.apps_dashboard import apps_dashboard
from subs.apps_plot import apps_plot
from subs.apps_plotly import apps_plotly

app = Flask(__name__)

Company.read(filename + 'DATABASEFINAL.db')
Warehouse.read(filename + 'DATABASEFINAL.db')
Order.read(filename + 'DATABASEFINAL.db')
Vehicle.read(filename + 'DATABASEFINAL.db')
Userlogin.read(filename + 'DATABASEFINAL.db')
import bcrypt
pass_encriptada = bcrypt.hashpw("1234".encode(), bcrypt.gensalt()).decode()
Userlogin(999, "g11", "g11", pass_encriptada)

app.secret_key = 'BAD_SECRET_KEY'
@app.route("/")
def index():
    return render_template("index.html", ulogin=session.get("user"))
@app.route("/login")
def login():
    return render_template("login.html", user= "", password="", ulogin=session.get("user"),resul = "")
@app.route("/logoff")
def logoff():
    session.pop("user",None)
    return render_template("index.html", ulogin=session.get("user"))
@app.route("/chklogin", methods=["post","get"])
def chklogin():
    user = request.form["user"]
    password = request.form["password"]
    resul = Userlogin.chk_password(user, password)
    if resul == "Valid":
        session["user"] = user
        return render_template("index.html", ulogin=session.get("user"))
    return render_template("login.html", user=user, password = password, ulogin=session.get("user"),resul = resul)
@app.route("/Company", methods=["post","get"])
def company():
    return apps_company()
@app.route("/gform/<cname>", methods=["post","get"])
def gform(cname):
    return apps_gform(cname)
@app.route("/subform/<cname>", methods=["post","get"])
def subform(cname):
    return apps_subform(cname)
@app.route("/Userlogin", methods=["post","get"])
def userlogin():
    return apps_userlogin()
@app.route("/dashboard")
def dashboard():
    return apps_dashboard()
@app.route("/plot")
def plot():
    return apps_plot()
@app.route("/plotly")
def plotly():
    return apps_plotly()
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
