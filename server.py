from flask import Flask, render_template,request
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    name = None
    message = None
    guests = []
    load_dotenv()

    #print(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"))

    # Connect to your database
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")) # do we need this?
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        message = request.form.get("message", "")
        cur.execute("INSERT INTO guests (name, message) VALUES (%s, %s)", (name, message))
        conn.commit()

    # Fetch all guests to display
    cur.execute("SELECT * FROM guests ORDER BY id DESC")
    guests = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("hello.html", name=name, guests=guests)
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)