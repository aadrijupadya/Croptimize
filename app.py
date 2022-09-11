import en_core_web_sm
import pandas as pd
import spacy
from flask import Flask, render_template, request, url_for, redirect, session, flash, send_from_directory
from flask_mysqldb import MySQL
from datetime import timedelta
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os
import tensorflow as tf



app = Flask(__name__)
app.secret_key = "appathon"
app.permanent_session_lifetime = timedelta(days=5)


app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = "root"
app.config['MYSQL_PASSWORD'] = "Aadrij2005"
app.config['MYSQL_DB'] = "learn_users"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)
res = []


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, "Only Images Are Allowed"),
            FileRequired("Field should not be empty")
        ]
    )
    submit = SubmitField("Upload")

@app.route('/', methods=["GET", "POST"])
def home():
    if "loggedin" in session:
        form = UploadForm()
        result = ""
        if form.validate_on_submit():
            print("working")
            filename = photos.save(form.photo.data)
            result = pre_image('uploads/'+filename, loaded_model)
            print(result)

            file_url = url_for('get_file', filename=filename)
        else:
            file_url = None
            print("not working")
        return render_template("loggedin.html", username=session["username"], form=form, file_url=file_url, result=result)

    else:
        return render_template("index.html")
    return render_template("index.html")