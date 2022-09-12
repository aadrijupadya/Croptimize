from flask import Flask, render_template, request, url_for, redirect, session, flash, send_from_directory
from flask_mysqldb import MySQL
from datetime import timedelta
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os
import tensorflow as tf
import numpy as np
import PIL
from PIL import Image
import numpy as np
import pickle
import xgboost
import sklearn
import PIL
from bs4 import BeautifulSoup

import csv
from io import StringIO
from flask_mysqldb import MySQL
from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians
import urllib.parse
from email.message import EmailMessage
import ssl
import smtplib
import en_core_web_sm
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os
import requests

# import tensorflow as tf
# from tensorflow import keras
month_dict = {868: 'January',
              603: 'February',
              1079: 'March',
              57: 'April',
              1102: 'May',
              895: 'June',
              893: 'July',
              87: 'August',
              1578: 'September',
              1275: 'October',
              1261: 'November',
              491: 'December'}
filename1 = 'weather_prediction.sav'
filename2 = 'weather_county_mappings.pickle'
filename3 = 'plant_disease_model.sav'
filename4 = 'crop_prediction.sav'

crop_model = pickle.load(open(filename4, 'rb'))
weather_model = pickle.load(open(filename1, 'rb'))
county_dict2 = pickle.load(open(filename2, 'rb'))
loaded_model = pickle.load(open(filename3, 'rb'))
county_dict = pickle.load(open('crop_county.sav', 'rb'))
crop_items = pickle.load(open('crop_items.sav', 'rb'))
county_map_crop = {v: k for k, v in county_dict.items()}
county_map_weather = {v: k for k, v in county_dict2.items()}
month_map_weather = {v: k for k, v in month_dict.items()}
county_map_items = {v: k for k, v in crop_items.items()}

app = Flask(__name__)
app.secret_key = "firewatch"

app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)
res = []


app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config['MYSQL_PASSWORD'] = "Aadrij2005"
app.config['MYSQL_DB'] = "fire_info"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


def get_weather_predictions(county_name, month):
    a = np.array([[county_map_weather[county_name], month_map_weather[month]]])
    weather_prediction = weather_model.predict(a)
    # print("Temperature (ºF): ", format(weather_prediction[0][0], 'f'), "Dewpoint (ºF): ", format(
    #     weather_prediction[0][1], 'f'), "Precipitation (in/month): ", format(weather_prediction[0][2] * 30, 'f'))
    weather_string = "Temperature (ºF): ", format(weather_prediction[0][0], 'f'), "Dewpoint (ºF): ", format(
        weather_prediction[0][1], 'f'), "Precipitation (in/month): ", format(weather_prediction[0][2] * 30, 'f')
    return weather_string

# get_weather_predictions('Contra Costa', 'July')


def get_crop_predictions(county, item):
    a = np.array([[county_map_crop[county], county_map_items[item]]])
    crop_prediction = crop_model.predict(a)
    crop_string = "Predicted yield of given crop in CWT/ACRE: ", crop_prediction[0]
    return crop_string


# get_crop_predictions(
#     'NASH', 'POTATOES, IRRIGATED - YIELD, MEASURED IN CWT / ACRE')

def get_predictions(path):
    img = tf.keras.utils.load_img(
        path,
        grayscale=False,
        color_mode="rgb",
        target_size=(250, 250),
        interpolation="nearest"
    )
    input_arr = tf.keras.preprocessing.image.img_to_array(img)
    input_arr = np.array([input_arr])

    predictions = loaded_model.predict(input_arr)
    predictions_list = list(predictions[0])
    prediction = predictions_list.index(max(predictions_list))
    return prediction

#

# get_predictions(
#     '/Users/aadrijupadya/Downloads/archive-3/test/test/TomatoYellowCurlVirus1.JPG')


def firewatch(loc_lat, loc_lon):
    app = Flask(__name__)
    app.secret_key = "firewatch"

    app.config["MYSQL_HOST"] = 'localhost'
    app.config["MYSQL_USER"] = "root"
    app.config['MYSQL_PASSWORD'] = "Aadrij2005"
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
                            a = sin(dlat / 2)**2 + cos(lat1) * \
                                cos(lat2) * sin(dlon / 2)**2
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
                                    smtp.sendmail(
                                        email_sender, email_receiver, em.as_string())
                    else:
                        per = out[4].split(":")[-1]
                        if "100%" in per:
                            print("no problem")
                        else:
                            dlon = lon2 - lon1
                            dlat = lat2 - lat1
                            a = sin(dlat / 2)**2 + cos(lat1) * \
                                cos(lat2) * sin(dlon / 2)**2
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
                                    smtp.sendmail(
                                        email_sender, email_receiver, em.as_string())
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
                                a = sin(dlat / 2)**2 + cos(lat1) * \
                                    cos(lat2) * sin(dlon / 2)**2
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
                                        smtp.login(
                                            email_sender, email_password)
                                        smtp.sendmail(
                                            email_sender, email_receiver, em.as_string())
                        else:
                            per = out[4].split(":")[-1]
                            if "100%" in per:
                                print("no problem")
                            else:
                                dlon = lon2 - lon1
                                dlat = lat2 - lat1
                                a = sin(dlat / 2)**2 + cos(lat1) * \
                                    cos(lat2) * sin(dlon / 2)**2
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
                                        smtp.login(
                                            email_sender, email_password)
                                        smtp.sendmail(
                                            email_sender, email_receiver, em.as_string())
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
                                a = sin(dlat / 2)**2 + cos(lat1) * \
                                    cos(lat2) * sin(dlon / 2)**2
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
                                        smtp.login(
                                            email_sender, email_password)
                                        smtp.sendmail(
                                            email_sender, email_receiver, em.as_string())
                        else:
                            per = out[4].split(":")[-1]
                            if "100%" in per:
                                print("no problem")
                            else:
                                dlon = lon2 - lon1
                                dlat = lat2 - lat1
                                a = sin(dlat / 2)**2 + cos(lat1) * \
                                    cos(lat2) * sin(dlon / 2)**2
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
                                        smtp.login(
                                            email_sender, email_password)
                                        smtp.sendmail(
                                            email_sender, email_receiver, em.as_string())

            except Exception as e:
                print(e)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, "Only Images Are Allowed"),
            FileRequired("Field should not be empty")
        ]
    )
    submit = SubmitField("Upload")


@app.route("/", methods=["GET", "POST"])
def home():
    if "loggedin" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM firewatch;")
        form = UploadForm()
        result = ""
        if form.validate_on_submit():
            print("working")
            filename = photos.save(form.photo.data)

            file_url = url_for('get_file', filename=filename)
            result = get_predictions(file_url)

        else:
            file_url = None
            print("not working")
        return render_template("loggedin.html", username=session["username"], form=form, file_url=file_url, result=result)

    else:
        return render_template("about.html")
    return render_template("about.html")


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


@app.route('/about')
def about():
    return render_template("about.html")


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


@app.route("/uploads/<filename>")
def get_file(filename):
    return send_from_directory("uploads", filename)


@app.route('/firewatch', methods=["GET", "POST"])
def weath_watch():
    if request.method == "POST":
        address = request.form["address"]
        url = 'https://nominatim.openstreetmap.org/search/' + \
            urllib.parse.quote(address) + '?format=json'
        response = requests.get(url).json()
        lat_a = response[0]['lat']
        lon_a = response[0]['lon']
        int_lata = int(float(lat_a))
        int_lona = int(float(lon_a))
        firewatch(int_lata, int_lona)
        return redirect(url_for('view'))
    return render_template("firewatch.html")


@app.route("/croppred", methods=["GET", "POST"])
def croppred():
    if "loggedin" in session:
        if request.method == "POST":
            county = request.form["county"]
            item = request.form["item"]
            crop_result = get_crop_predictions(county, item)
            return render_template("croppred.html", crop_result=crop_result)
        else:
            return render_template("croppred.html")
    else:
        return render_template("about.html")


@app.route("/weathpred", methods=["GET", "POST"])
def weathpred():
    if "loggedin" in session:
        if request.method == "POST":
            county = request.form["county"]
            month = request.form["month"]
            weather_result = get_weather_predictions(county, month)
            print(weather_result)
            return render_template("weathpred.html", weather_result=weather_result)
        else:
            return render_template("weathpred.html")
    else:
        return render_template("about.html")


@app.route('/view', methods=["GET", "POST"])
def view():
    if "loggedin" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM firewatch")
        fires = cursor.fetchall()
        for row in fires:
            print(row)
        return render_template("view.html", fires=fires)
    else:
        return render_template("about.html")


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    session.pop("gmail", None)
    session.pop("registered", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
