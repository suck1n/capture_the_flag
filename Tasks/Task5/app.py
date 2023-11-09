import collections
import datetime
import os
import re
import socket
import sqlite3
import subprocess
import uuid

import bcrypt
import dotenv
from flask import Flask, request, session, redirect, flash, render_template_string, g

from static import PROFILE_PAGE, LOGIN_PAGE, REGISTER_PAGE, COMPLAINT_PAGE, EDIT_PAGE

app = Flask(__name__)
app.config["SESSION_COOKIE_SAMESITE"] = "Strict"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=60)

ROLE_USER = "User"
ROLE_ADMIN = "Admin"
DEFAULT_PICTURE = "data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjAgMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iIzAwNTZiZCIvPjxwYXRoIGQ9Ik0xMC44OTQgMTEuNzc5cS0uMDcxLjQ0NC0uMzAyLjcyOC0uMjMxLjI4NS0uNjQ5LjI4NS0uMTYgMC0uMzItLjA0NS0uODYyLS4yMjItLjg2Mi0xLjAzIDAtLjI0LjA4LS41NDMuMTI0LS41MDYuMzY0LS45NDIuMjUtLjQ0NC41MzQtLjc1NS4yOTMtLjMyLjYxMy0uNjA0LjMyLS4yODUuNjA0LS41MjUuMjkzLS4yNDguNTMzLS40ODguMjQtLjI0LjM3NC0uNTM0LjE0Mi0uMjkzLjE0Mi0uNjEzIDAtLjgtLjQ1My0xLjIyNi0uNDU0LS40MjctMS41Mi0uNDI3LS4yODUgMC0uNTUxLjEzMy0uMjY3LjEzNC0uNTA3LjM5MS0uMjQuMjUtLjQwOS40NzItLjE2OC4yMTMtLjM4Mi41NDItLjM5LjU4Ni0uODM1LjU4Ni0uMjEzIDAtLjU5NS0uMTY5LS40OS0uMjQ5LS40OS0uNzczIDAtLjMyLjE5Ni0uNjg0LjE1MS0uMzAyLjM2NS0uNTk2LjIxMy0uMjkzLjU0Mi0uNjEzLjMyOS0uMzIuNjkzLS41Ni4zNzMtLjI0Ljg3LS4zOS40OTktLjE2IDEuMDIzLS4xNiAyLjAyNiAwIDMuMDg0Ljk2IDEuMDY2Ljk1IDEuMDY2IDIuODI1IDAgLjUxNi0uMTYuOTMzLS4xNi40MTgtLjQxOC43MTEtLjI1Ny4yOTQtLjU3Ny41NTEtLjMxMS4yNTgtLjY0OS41MTYtLjMyOS4yNDktLjYyMi41MjQtLjI4NC4yNjctLjUwNy42NTgtLjIxMy4zOS0uMjc1Ljg2MnpNOS44MjcgMTYuNjNxLS4wOC4wMDktLjE3Ny4wMDktLjY2NyAwLTEuMDg1LS40NzEtLjQwOC0uNDgtLjQwOC0xLjA5MyAwLS42MjIuNTA2LTEuMDU4LjUwNy0uNDM1IDEuMTQ3LS40N2guMDhxLjY2NiAwIDEuMDg0LjQ0NC40MjYuNDM1LjQyNiAxLjA2NiAwIC42MjItLjQzNSAxLjA2Ni0uNDI3LjQzNi0xLjEzOC41MDd6IiB0cmFuc2Zvcm09InNjYWxlKC45OTU1NiAxLjAwNDQ2KSIgZmlsbD0iI2ZmZiIvPjwvc3ZnPg=="

UserData = collections.namedtuple("UserData", ("username", "picture", "grade", "role"))

# Setup Server, by creating secret key, admin password and database
if not os.path.exists("app-secret.key"):
    with open("app-secret.key", "wb") as f:
        f.write(os.getrandom(32))

with open("app-secret.key", "rb") as f:
    app.secret_key = f.read()

if not os.path.exists("admin-password.txt"):
    with open("admin-password.txt", "wb") as f:
        f.write(os.getrandom(16).hex().encode())

with open("admin-password.txt", "rb") as f:
    admin_password = bcrypt.hashpw(f.read().strip(), bcrypt.gensalt()).decode()

if not os.path.exists("db"):
    os.mkdir("db")

# Function to create a new UUID (User-Unique-Identification-Number)
new_uid = lambda: str(uuid.uuid4())

# Get Database Object
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("db/users.db", isolation_level=None)
        db.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY NOT NULL, username TEXT, password TEXT, picture TEXT, grade TEXT, role TEXT, UNIQUE (id), UNIQUE(username))")
        db.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)", (new_uid(), "admin", admin_password, DEFAULT_PICTURE, "9.75", ROLE_ADMIN))
    return db

# Check if username and password are correct (SQL Injection not possible)
def check_login(username, password):
    cursor = get_db().execute("SELECT id, password, role FROM users WHERE username = ? LIMIT 1", (username,))
    result = cursor.fetchone()
    if result: 
        user_id, target_hash, role = result
        is_ok = bcrypt.checkpw(password.encode(), target_hash.encode())
        return (user_id, role) if is_ok and user_id else None
    else:
        return None

# Create a user if it does not exist (SQL Injection not possible)
def create_user(username, password):
    cursor = get_db().execute("INSERT OR IGNORE INTO users (id, username, password, picture, grade, role) VALUES (?, ?, ?, ?, ?, ?)", (new_uid(), username, bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), DEFAULT_PICTURE, "4.0", ROLE_USER))    
    return cursor.rowcount == 1

# Get Data of a User. Data includes: username, picture, grade and role
def get_data(user_id):
    cursor = get_db().execute("SELECT username, picture, grade, role FROM users WHERE id = ?", (user_id,))
    try:
        username, picture, grade, role = cursor.fetchone()
    except TypeError:
        raise KeyError(f"No such user: {user_id}")
    return UserData(username, picture, grade, role)

# Edit the user data
def edit_user(user_id, username, password, picture):
    cursor = get_db().cursor()
    if password:
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), user_id))
        if cursor.rowcount != 1:
            return "Failed to update password"
    cursor.execute("UPDATE users SET picture = ? WHERE id = ?", (picture, user_id))
    if cursor.rowcount != 1:
        return "Failed to update picture"
    try:
        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
    except sqlite3.IntegrityError:
        return "Failed to update username"
    if cursor.rowcount != 1:
        return "Failed to update username"
    return "Profile updated"

@app.route("/")
def index():
    # if not logged in, redirect to login page
    if "user_id" not in session:
        return redirect("/login")
    
    # if user does not exist redirect to login page
    try:
        get_data(session["user_id"])
    except KeyError:
        return redirect("/login")

    # else redirect to profile page
    return redirect(f"/profile/{session['user_id']}")

@app.route("/profile/<target_id>")
def profile(target_id):
    # if not logged in, redirect to login page
    if "user_id" not in session:
        return redirect("/login")
    
    # get the user id of the target
    try:
        target_id = str(uuid.UUID(target_id)) # canonicalize
    except ValueError:
        return "Bad profile link", 400
        
    # check if user is allowed to see the profile of target_id
    if session["user_id"] != target_id:
        if session["role"] != ROLE_ADMIN:
            # Only admin is allowed to see other user's profiles
            return "Permission denied", 403
            
    # get user data
    try:
        data = get_data(target_id)
    except KeyError:
        return "No such user", 404
    
    # if the grade is a 10.0, then set a flag
    flag = ""
    if data.grade == "10.0":
        flag = subprocess.check_output(["/bin/flag", "5"]).decode().strip()
    return render_template_string(PROFILE_PAGE, data=data, flag=flag)

@app.route("/logout")
def logout():
    # remove session cookie = logout
    session.clear()
    return redirect("/login")

# not relevant for task
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("No username or password specified")
        if login_result := check_login(username.strip(), password):
            user_id, role = login_result
            session.permanent = True
            session["user_id"] = user_id
            session["role"] = role
            return redirect("/")
        else:
            flash("Incorrect username or password")
    return render_template_string(LOGIN_PAGE)

# not relevant for task
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("No username or password specified")
        elif len(password) < 12:
            flash("Password must have at least 12 characters")
        elif create_user(username.strip(), password):
            flash("User created, please log in")
            return redirect("/login")
        else:
            flash("Could not create user, please try a different username")
    return render_template_string(REGISTER_PAGE)


@app.route("/complain", methods=["GET", "POST"])
def complain():
    # if user is not logged in, redirect to login page
    if "user_id" not in session:
        return redirect("/login")
        
    # get user data
    data = get_data(session["user_id"])
    
    # if it is a POST Request
    if request.method == "POST":
        # Forward the complaint to the admin
        # Request needs a field with key = "complaint", value = actual complaint text
        if "complaint" in request.form:
            print(f"\x1b[33mComplaint by user {session['user_id']} ({data.username}, {data.grade}):\x1b[0m {request.form['complaint']!r}")

        # connection to send the complaint to the 'admin' (server which handles the complaint)
        address = (os.environ["ADMIN_CONTACT_HOST"], int(os.environ["ADMIN_CONTACT_PORT"]))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(address)
            sock.sendall(session["user_id"].encode() + b"\n")
            
        # notify user complaint has been sent by 'flashing' the text Complaint sent
        flash("Complaint sent")
        
        # redirect to profile page
        return redirect(f"/profile/{session['user_id']}")
    
    # load complaint page
    return render_template_string(COMPLAINT_PAGE, data=data)

# endpoint to set the grade of a student
@app.route("/set-grade")
def set_grade():
    # if not logged in, redirect
    if "user_id" not in session:
        return redirect("/login")
    
    # if the user is not a admin, send permission denied
    if session.get("role") != ROLE_ADMIN:
        return "Permission denied", 403
    
    # get user id and new grade from url
    # url must be http://[HOST]:[PORT]/set-grade?user=[USER_ID]&grade=[NEW_GRADE]
    user_id = request.args.get("user")
    new_grade = request.args.get("grade")
    
    if not user_id or not new_grade:
        return "No user or grade specified", 400
    # if grade has not the format of a grade between 4.0 and 10.0
    elif not re.match(r"^(?:[456789]\.\d\d?)|(?:10\.00?)$", new_grade):
        return "Invalid grade", 400
        
    
    try:
        user_id = str(uuid.UUID(user_id)) # canonicalize
    except ValueError:
        return "Invalid user", 400
   
    # update the grade of the user
    cursor = get_db().execute("UPDATE users SET grade = ? WHERE id = ?", (new_grade, user_id))
    
    if cursor.rowcount == 1:
        return "", 204 # No content
    else:
        return "Invalid user", 400

@app.route("/edit", methods=["GET", "POST"])
def edit():
    # if not logged in, redirect
    if "user_id" not in session:
        return redirect("/login")
    
    # get current user data
    data = get_data(session["user_id"])
    
    # if it is a POST request
    if request.method == "POST":
        # and 'username' or 'password' or 'picture' have a value
        if request.form.get("username") or request.form.get("password") or request.form.get("picture"):
            # update the user data
            username = request.form.get("username") or data.username # Unchanged if empty
            password = request.form.get("password") or None
            picture = request.form.get("picture") or DEFAULT_PICTURE # Default if empty
            
            message = edit_user(session["user_id"], username.strip(), password, picture.strip())
            if message:
                flash(message)
        return redirect(f"/profile/{session['user_id']}")
    return render_template_string(EDIT_PAGE, data=data)


if __name__ == "__main__":
    dotenv.load_dotenv(".env.local")
    app.run("0.0.0.0", 5005)
