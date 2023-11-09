#!/usr/bin/env python3

from flask import Flask, request
import subprocess
import sqlite3

app = Flask(__name__)

page_head = """
<!doctype html>
<html>
<head>
<title>Fallmoogle!</title>
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
    <h1>Fallmoogle!</h1>
    <h2>The <i>excellent</i> search engine!</h2>
    <form action="/" method="get">
        <input type="text" name="q">
        <input type="submit" value="Search!">
    </form>
<div id="results">"""

page_footer = """
</div>
</body>
</html>
"""

def load_intranet(db):
    db.execute("CREATE TABLE intranet_index (id INT PRIMARY KEY, title TEXT, url TEXT, is_secret INT)")
    flag = subprocess.check_output(["/bin/flag", "1"]).decode()
    db.execute("""INSERT INTO intranet_index VALUES
    (NULL, "Very Cool Site", "http://www.fallmerayer.it", 0),
    (NULL, "Digital Register", "http://www.digitalesregister.it", 0),
    (NULL, "Some", "http://www.website.it", 0),
    (NULL, "Stack Overflow", "http://www.stackoverflow.com", 0),
    (NULL, "Best site out there", "http://10.10.30.38", 0),
    (NULL, "Wikipedia", "http://www.wikipedia.de", 0),
    (NULL, "{}", "", 1)
    """.format(flag))

@app.route("/")
def index():
    q = request.args.get("q")
    print(q)
    page = ""
    if q:
        if len(q) >= 3:
            db = sqlite3.connect(":memory:", isolation_level=None)
            load_intranet(db)
            cur = db.cursor()
            cur.execute("SELECT * FROM intranet_index WHERE is_secret=0 AND title LIKE '%{}%'".format(q))
            page += "<h2>Results</h2>"
            for record in cur.fetchall():
                page = page + """<a href="{}">{}</a><br>""".format(record[2], record[1])
        else:
            page = "Search query to short!"
    return page_head + page + page_footer

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
