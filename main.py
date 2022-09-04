from flask import Flask, render_template, request, url_for, redirect, session
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "firewatch"

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)