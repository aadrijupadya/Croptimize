from flask import Flask, render_template, request, url_for, redirect, session
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
import csv
from io import StringIO
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = "firewatch"

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config['MYSQL_PASSWORD'] = "ffrn1234"
app.config['MYSQL_DB'] = "fire_info"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

def firewatch():
    info_list = []
    url = "https://www.fire.ca.gov/incidents/2022/"
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content, "html.parser")
    scripts = soup.find_all("script")
    str_scripts = str(scripts)
    with open("califire.txt", "w") as f:
        f.write(str_scripts)
        f.close()
    with open("califire.txt", "r") as read:
        for line in read:
            info_list.extend(line.split())

    for idx, v in enumerate(info_list):
        if "Latitude" in v:
            line1 = info_list[idx]

            reader = csv.reader(StringIO(line1))
            out = next(reader)
            try:
                if "Longitude" in out[1]:
                    # print(out[0] + "||" + out[1] + ".")
                    lat = out[0].split(':')[-1]
                    lon = out[1].split(":")[-1]
                    print(lat + "||" + lon )
                else:
                    # print(out[1]+"| |" + out[2] + "..")
                    lat = out[1].split(':')[-1]
                    lon = out[2].split(":")[-1]
                    print(lat + "||" + lon )

                if "PercentContainedDisplay" in out[3]:
                    print(out[2] + "||" + out[3] + ".")
                else:
                    print(out[3] + "||" + out[4] + "..")
                    print("-----------------------------------------------------------")
            except:
                print("latitude not in index")


@app.route("/", methods=["GET", "POST"])
def home():
    if "loggedin" in session:
        return render_template("inhome.html", username = session["username"])
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if 'registered' in session:
            print("you've been redirected")
            return redirect(url_for("login"))
    elif request.method == "POST":
        first = request.form["first"]
        email = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO userlist(name, gmail, password) VALUES(%s, %s, %s) ''',
                       (first, email, password))
        mysql.connection.commit()
        session["registered"] = True
        print("in session")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ''
    if request.method == "GET":
        if "loggedin" in session:
            return redirect(url_for('home'))
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM userlist WHERE gmail=%s AND password=%s", (email, password,))
        record = cursor.fetchone()
        try:
            rec_list = list(record.keys())
            val_list = list(record.values())
            ind = rec_list.index("name")
            user = val_list[ind]
            print(user)
        except:
            print("retry")
        if record:
            print(record)
            session["loggedin"] = True
            session["username"] = user
            return redirect(url_for("home"))
        else:
            print("Retry")
    return render_template("login.html", msg=msg)

@app.route('/firewatch', methods = ["GET", "POST"])
def weath_watch():
    if request.method == "POST":
        firewatch()
    return render_template("firewatch.html", firewatch = firewatch())

@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    session.pop("registered", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)