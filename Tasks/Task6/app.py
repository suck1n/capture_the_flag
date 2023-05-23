import os
import socket
import string
import subprocess

import bcrypt
import dotenv
from flask import Flask, request, session, redirect

app = Flask(__name__)

if not os.path.exists("app-secret.key"):
    with open("app-secret.key", "wb") as f:
        f.write(os.urandom(32))

with open("app-secret.key", "rb") as f:
    app.secret_key = f.read()

if not os.path.exists("admin-password.txt"):
    with open("admin-password.txt", "wb") as f:
        f.write(os.getrandom(16).hex().encode())

with open("admin-password.txt", "rb") as f:
    admin_password = bcrypt.hashpw(f.read().strip(), bcrypt.gensalt())

allowed_users = {
    "admin": admin_password,
    "testuser": bcrypt.hashpw(b"foobar", bcrypt.gensalt())
}

# Just html code, can be ignored = not relevant for the task
prelude = """<!DOCTYPE html>
<html>
<head>
<title>Bank.de (offered by I20)</title>
</head>
<body>
<h1>Bank.de</h1>
<h2>Trusted banking by TUM</h2>
"""

epiloge = """</body>
</html>"""

main_site = string.Template("""<b>Your account 11235813:</b>
<table>
<tr>
<th>Date</th>
<th>Receiver/Sender</th>
<th>Transaction Description</th>
<th>Amount</th>
</tr>
<tr>
<td>01.10.2019</td>
<td>Fabian Franzen</td>
<td>Plz give me 1.0 in the exam!</td>
<td><font color="red">-1337.0 €</font></td>
</tr>
<tr>
<td>02.10.2019</td>
<td>Fabian Franzen</td>
<td>Nope! Plz learn more!</td>
<td>+1337.0 €</td>
</tr>
</table>
<div id="balance"><b>Balance: ${amount}€</b></div>

<p>Your selected language is: ${ln}</p>
<br>
<a href="/logout">Logout</a><br>
Any problem with our site? <a href="/contact">Contact our admin</a> if you have questions!
""")

login_site = """<form method="post" action="/login">
<input type="text" name="username" placeholder="Username">
<input type="password" name="password" placeholder="Password">
<input type="submit" value="login">
</form>

Do you want to test our product?<br>
Login using username <code>testuser</code> with password <code>foobar</code>.
"""

contact_site = """
Any problem with our service? Our admin will be happy to assist you.
<form method="post" action="/contact">
<textarea name="contacttext" rows="8" cols="90"></textarea>
<br>
<input type="submit" value="Send">
</form>"""


@app.route("/")
def index():
    # if not logged in, redirect
    if "user" not in session:
        return redirect("/login")

    # get set language, if not set default to English
    d = {
        "ln": request.args.get("ln", "English")
    }

    # Check if the user is "admin" => if so create flag otherwise set 0
    if session["user"] == "admin":
        d["amount"] = subprocess.check_output(["/bin/flag", "6"]).decode()
    else:
        d["amount"] = "0"

    # Never do this at home, it might have some security problems...
    return prelude + main_site.substitute(d) + epiloge


@app.route("/logout")
def logout():
    if "user" in session:
        del session["user"]
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Login via POST request
    if request.method == "POST":
        # Get username
        username = request.form["username"]
        # and password
        pw = request.form["password"]

        # username must be in the allowed users
        if username in allowed_users:
            # check against hashed password
            if bcrypt.checkpw(pw.encode(), allowed_users[username]):
                # on success redirect
                session.permanent = True
                session["user"] = username
                return redirect("/?ln=English")
            else:
                raise ValueError(f"Bad password: {pw!r}")

    return prelude + login_site + epiloge


@app.route("/contact", methods=["GET", "POST"])
def contact():
    # If it is a POST request
    if request.method == "POST":
        # Forward the link to the admin
        # Link must be sent with the key = "contacttext"
        text = request.form["contacttext"]

        # Sending the Link to the "admin" (my server in the background)
        address = (os.environ['ADMIN_CONTACT_HOST'], int(os.environ['ADMIN_CONTACT_PORT']))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.sendall(text.encode())
        sock.close()

    return prelude + contact_site + epiloge


if __name__ == "__main__":
    dotenv.load_dotenv(".env.local")
    app.run("127.0.0.1", 5006)
