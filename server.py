from flask import Flask, render_template,request,session, redirect, url_for
import db
from db import setup, get_db_cursor
import psycopg2
from dotenv import load_dotenv, find_dotenv
import os
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)


db.setup() #if using daniel's db example
with get_db_cursor() as cur:
    cur.execute("SELECT current_database();")
    print("Connected to DB:", cur.fetchone()[0])


### AUTH STUFF ###
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for("hello"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.environ.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("hello", _external=True),
                "client_id": os.environ.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/") #, methods=["GET", "POST"])
#def index():
#    name = None
#    message = None
#    guests = []
#    load_dotenv()
#
    #print(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"))
#
    # From .env file
#    conn = psycopg2.connect(
#        dbname=os.getenv("DB_NAME"),
#        user=os.getenv("DB_USER"),
#        password=os.getenv("DB_PASSWORD"),
#        host=os.getenv("DB_HOST"),
#        port=os.getenv("DB_PORT")) # do we need this?
#    cur = conn.cursor()

#    if request.method == "POST":
#        name = request.form["name"]
#        message = request.form.get("message", "")
#        cur.execute("INSERT INTO guests (name, message) VALUES (%s, %s)", (name, message))
#        conn.commit()

    # Fetch all guests to display
#    cur.execute("SELECT * FROM guests ORDER BY id DESC")
#    guests = cur.fetchall()

#    cur.close()
#    conn.close()

#    return render_template("hello.html", name=name, guests=guests)
@app.route('/<name>')
def hello(name=None):
    return render_template('hello.html', name=name, guestlist=db.get_guestbook())

@app.post("/submit")
def submit():
    name = request.form.get("name")
    text = request.form.get("text")
    db.add_post(name, text)
    return render_template("hello.html", name=None, guestlist=db.get_guestbook())

@app.route("/pure-grid")
def pure_grid():
    return render_template("pure-grid.html")