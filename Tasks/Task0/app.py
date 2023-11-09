#!/usr/bin/env python3

from flask import Flask, request
import subprocess

app = Flask(__name__)

page_head = """
<!DOCTYPE html>
<html>
<head>
    <title>Some Random Webpage of the Internet</title>
</head>
<body>
    <main style="left: 50%;position: absolute;top: 50%;transform: translate(-50%, -50%);font-size: 24px;">
    <h1>Some Random Webpage of the Internet</h1>
    Hmm, it's so empty here. There is nothing interesting here, I promise! 
"""
   
page_footer = """
    </main>
</body>
</html>
"""

@app.route("/")
def index():
    flag = subprocess.check_output(["/bin/flag", "0"]).decode()
    return page_head + "<!--" + flag + "-->" + page_footer
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
