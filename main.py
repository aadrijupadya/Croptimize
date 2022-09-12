from flask import Flask, render_template, request, url_for, redirect, session
from datetime import timedelta
from bs4 import BeautifulSoup
import requests
import csv
from io import StringIO
from flask_mysqldb import MySQL
from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians
import urllib.parse
from email.message import EmailMessage
import ssl
import smtplib


app = Flask(__name__)
app.secret_key = "firewatch"

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config['MYSQL_PASSWORD'] = "ffrn1234"
app.config['MYSQL_DB'] = "fire_info"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

def firewatch(loc_lat, loc_lon):
    app = Flask(__name__)
    app.secret_key = "firewatch"

    app.config["MYSQL_HOST"] = 'localhost'
    app.config["MYSQL_USER"] = "root"
    app.config['MYSQL_PASSWORD'] = "ffrn1234"
    app.config['MYSQL_DB'] = "fire_info"
    app.config['MYSQL_CURSORCLASS'] = "DictCursor"
    mysql = MySQL(app)


    email_sender = 'croptimizecorp@gmail.com'
    email_password = "gtgxkleezkwxzssd"
    email_receiver = session["gmail"]

    subject = "Potential Danger From Fire Nearby"
    body = """
    This Alert Was Sent Because Your Property Might Be In Danger, There Is A Fire Within 10 Miles Of You. 
    """
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()


    R = 6373.0
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


                if "Longitude" in out[1] and "PercentContainedDisplayed" in out[3]:
                    # print(out[0] + "||" + out[1] + ".")
                    lat = out[0].split(':')[-1]
                    lon = out[1].split(":")[-1]
                    per = out[3].split(":")[-1]
                    int_lat = int(float(lat))
                    int_lon = int(float(lon))
                    lat1 = radians(int_lat)
                    lon1 = radians(int_lon)
                    lat2 = radians(loc_lat)
                    lon2 = radians(loc_lon)
                    email = session["gmail"]
                    if "%" in per:
                        if "100%" in per:
                            print("no problem")
                        else:
                            dlon = lon2 - lon1
                            dlat = lat2 - lat1
                            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                            c = 2 * atan2(sqrt(a), sqrt(1 - a))
                            distance = R * c
                            danger = 'No'
                            print("Result:", distance)
                            if distance < 16.0934:
                                danger = "Yes"
                                # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                #     smtp.login(email_sender, email_password)
                                #     smtp.sendmail(email_sender, email_receiver, em.as_string())        
                            print(per + ".")
                            lat_lon = lat + "," + lon
                            user_name = session['username']
                            cursor = mysql.connection.cursor()
                            cursor.execute(''' INSERT IGNORE INTO firewatch(user_name, lat_lon, percent_contained, fire_distance, danger) VALUES(%s, %s, %s, %s, %s) ''',
                       (user_name, lat_lon, per, distance, danger))
                            mysql.connection.commit()
                            if danger == "Yes":
                                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                    smtp.login(email_sender, email_password)
                                    smtp.sendmail(email_sender, email_receiver, em.as_string()) 
                    else:
                        per = out[4].split(":")[-1]
                        if "100%" in per:
                            print("no problem")
                        else:
                            dlon = lon2 - lon1
                            dlat = lat2 - lat1
                            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                            c = 2 * atan2(sqrt(a), sqrt(1 - a))
                            distance = R * c
                            danger = 'No'
                            print("Result:", distance)
                            if distance < 16.0934:
                                danger = "Yes"
                                # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                #     smtp.login(email_sender, email_password)
                                #     smtp.sendmail(email_sender, email_receiver, em.as_string())  
                            print(per + ".")
                            lat_lon = lat + "," + lon
                            user_name = session['username']
                            cursor = mysql.connection.cursor()
                            cursor.execute(''' INSERT IGNORE INTO firewatch(user_name, lat_lon, percent_contained, fire_distance, danger) VALUES(%s, %s, %s, %s, %s) ''',
                       (user_name, lat_lon, per, distance, danger))
                            mysql.connection.commit()
                            if danger == "Yes":
                                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                    smtp.login(email_sender, email_password)
                                    smtp.sendmail(email_sender, email_receiver, em.as_string()) 
                else:
                    if '"' in out[2]:
                        lat = out[0].split(':')[-1]
                        lon = out[1].split(':')[-1]
                        per = out[3].split(':')[-1]
                        int_lat = int(float(lat))
                        int_lon = int(float(lon))
                        lat1 = radians(int_lat)
                        lon1 = radians(int_lon)
                        lat2 = radians(loc_lat)
                        lon2 = radians(loc_lon)
                        if "%" in per:
                            if "100%" in per:
                                print("no problem")
                            else: 
                                dlon = lon2 - lon1
                                dlat = lat2 - lat1
                                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                                distance = R * c
                                danger = 'No'
                                print("Result:", distance)
                                if distance < 16.0934:
                                    danger = "Yes"
                                    # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                    #     smtp.login(email_sender, email_password)
                                    #     smtp.sendmail(email_sender, email_receiver, em.as_string()) 
                                print(per + ".")
                                lat_lon = lat + "," + lon
                                user_name = session['username']
                                cursor = mysql.connection.cursor()
                                cursor.execute(''' INSERT IGNORE INTO firewatch(user_name, lat_lon, percent_contained, fire_distance, danger) VALUES(%s, %s, %s, %s, %s) ''',
                        (user_name, lat_lon, per, distance, danger))
                                mysql.connection.commit()
                                if danger == "Yes":
                                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                        smtp.login(email_sender, email_password)
                                        smtp.sendmail(email_sender, email_receiver, em.as_string()) 
                        else:
                            per = out[4].split(":")[-1]
                            if "100%" in per:
                                print("no problem")
                            else:
                                dlon = lon2 - lon1
                                dlat = lat2 - lat1
                                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                                distance = R * c
                                danger = 'No'
                                print("Result:", distance)
                                if distance < 16.0934:
                                    danger = "Yes"
                                    # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                    #     smtp.login(email_sender, email_password)
                                    #     smtp.sendmail(email_sender, email_receiver, em.as_string()) 
                                print(per + ".")
                                lat_lon = lat + "," + lon
                                user_name = session['username']
                                cursor = mysql.connection.cursor()
                                cursor.execute(''' INSERT IGNORE INTO firewatch(user_name, lat_lon, percent_contained, fire_distance, danger) VALUES(%s, %s, %s, %s, %s) ''',
                        (user_name, lat_lon, per, distance, danger))
                                mysql.connection.commit()
                                if danger == "Yes":
                                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                        smtp.login(email_sender, email_password)
                                        smtp.sendmail(email_sender, email_receiver, em.as_string()) 
                    else:
                        lat = out[1].split(':')[-1]
                        lon = out[2].split(":")[-1]
                        per = out[4].split(":")[-1]
                        int_lat = int(float(lat))
                        int_lon = int(float(lon))
                        lat1 = radians(int_lat)
                        lon1 = radians(int_lon)
                        lat2 = radians(loc_lat)
                        lon2 = radians(loc_lon)
                        if "%" in per:
                            if "100%" in per:
                                print("no problem")
                            else:
                                dlon = lon2 - lon1
                                dlat = lat2 - lat1
                                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                                distance = R * c
                                danger = 'No'
                                print("Result:", distance)
                                if distance < 16.0934:
                                    danger = "Yes"
                                    # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                    #     smtp.login(email_sender, email_password)
                                    #     smtp.sendmail(email_sender, email_receiver, em.as_string()) 
                                print(per + ".")
                                lat_lon = lat + "," + lon
                                user_name = session['username']
                                cursor = mysql.connection.cursor()
                                cursor.execute(''' INSERT IGNORE INTO firewatch(user_name, lat_lon, percent_contained, fire_distance, danger) VALUES(%s, %s, %s, %s, %s) ''',
                        (user_name, lat_lon, per, distance, danger))
                                mysql.connection.commit()
                                if danger == "Yes":
                                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                        smtp.login(email_sender, email_password)
                                        smtp.sendmail(email_sender, email_receiver, em.as_string()) 
                        else:
                            per = out[4].split(":")[-1]
                            if "100%" in per:
                                print("no problem")
                            else:
                                dlon = lon2 - lon1
                                dlat = lat2 - lat1
                                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                                distance = R * c
                                danger = 'No'
                                print("Result:", distance)
                                if distance < 16.0934:
                                    danger = "Yes"
                                print(per + ".")
                                lat_lon = lat + "," + lon
                                user_name = session['username']
                                cursor = mysql.connection.cursor()
                                cursor.execute(''' INSERT IGNORE INTO firewatch(user_name, lat_lon, percent_contained, fire_distance, danger) VALUES(%s, %s, %s, %s, %s) ''',
                        (user_name, lat_lon, per, distance, danger))
                                mysql.connection.commit()
                                if danger == "Yes":
                                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                        smtp.login(email_sender, email_password)
                                        smtp.sendmail(email_sender, email_receiver, em.as_string()) 

            except Exception as e:
                print(e)


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
            rec_list1 = list(record.keys())
            val_list1 = list(record.values())
            ind1 = rec_list.index("gmail")
            gmail = val_list[ind1]
        except:
            print("retry")
        if record:
            print(record)
            session["loggedin"] = True
            session["username"] = user
            session['gmail'] = gmail 
            return redirect(url_for("home"))
        else:
            print("Retry")
    return render_template("login.html", msg=msg)

@app.route('/firewatch', methods = ["GET", "POST"])
def weath_watch():
    if request.method == "POST":
        address = request.form["address"]
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        response = requests.get(url).json()
        lat_a = response[0]['lat']
        lon_a = response[0]['lon']
        int_lata = int(float(lat_a))
        int_lona = int(float(lon_a))
        firewatch(int_lata, int_lona)
        return redirect(url_for('view'))
    return render_template("firewatch.html")

@app.route('/view', methods = ["GET", "POST"])
def view():
    if "loggedin" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM firewatch")
        fires = cursor.fetchall()
        for row in fires:
            print(row)
        return render_template("view.html", fires = fires)
    else:
        return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    session.pop("gmail", None)
    session.pop("registered", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)