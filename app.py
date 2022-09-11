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


@app.route('/', methods=["GET", "POST"])
def home():
    # if "loggedin" in session:
    #     return render_template(".html")
    # else:
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
