#!/usr/bin/python3

from flask import Flask, request, redirect, session
from flask_session import Session
import datetime
import subprocess
import sqlite3
import os
import binascii

ADMIN_USER = "admin"

PAGE_HEAD = """
<!doctype html>
<html>
<head>
<title>Fallmerayer+!</title>
<style>
body {
    text-align: center;
}

h1 {
    font-family: sans-serif;
    color: #0065bd;
}
#results {
    margin-top: 10px;
    text-align: left;
}
</style>

</head>

<body>
    <h1>Fallmerayer+!</h1>
    <h2>The <i>excellent</i> social network!</h2>
"""

LOGIN_FORM = """
    <form action="/" method="post">
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <input type="submit" value="Login">
    </form>
"""

PAGE_FOOTER = """
</body>
</html>
"""

app = Flask(__name__)

# Create secret key
if not os.path.exists("app-secret.key"):
    with open("app-secret.key", "wb") as f:
        f.write(os.getrandom(32))

with open("app-secret.key", "rb") as f:
    app.secret_key = f.read()


# Set session life time
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=20)
app.config["SESSION_TYPE"] = "filesystem"
Session(app) # Stores sessions in current working directory, which is OK for us.


# Creates database
def load_db(db, admin_user, admin_pass):
    db.execute("CREATE TABLE fallmerayerplus_users (id INT PRIMARY KEY, username TEXT, password TEXT)")
    db.execute("""INSERT INTO fallmerayerplus_users VALUES (1, "{}", "{}")""".format(admin_user, admin_pass))


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # Get username and password from post request
        username = request.form["username"]
        password = request.form["password"]

        # Get current admin password from session
        admin_pass = session.get('admin_pass')
        if admin_pass is None:
            admin_pass = os.getrandom(16).hex() # If there is none, create one randomly (so passwords cannot be shared)
            session['admin_pass'] = admin_pass
        
        # Connect to database
        db = sqlite3.connect(":memory:", isolation_level=None)
        load_db(db, ADMIN_USER, admin_pass)
        
        # Get user with username and password
        cur = db.cursor()
        cur.execute(f'SELECT * FROM fallmerayerplus_users WHERE username = "{username}"  and password="{password}"')
        
        # Fetch first result
        res = cur.fetchone()
        if res:
            # Check if it was the admin account
            if res[1] == username == ADMIN_USER and res[2] == password == admin_pass:
                flag = subprocess.check_output(["/bin/flag", "2"]).decode()
                print(flag)
                return PAGE_HEAD + "<b>Hi {}, here is your flag: {}</b>".format(username, flag) + PAGE_FOOTER
            else:
                return PAGE_HEAD + "<b>Hmm my database says you're admin, but of course I20 doesn't fall for your cheap tricks!!</b>" + PAGE_FOOTER
        else:
            return redirect("/")
    else:
        return PAGE_HEAD + LOGIN_FORM + PAGE_FOOTER


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
