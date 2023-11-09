from flask import Flask, render_template_string, session, request, flash, redirect
from Crypto.Cipher import AES
import os
import subprocess

# App metadata
if not os.path.exists('app-secret.key'):
    with open('app-secret.key', 'wb') as f:
        # Flask secret key
        f.write(os.urandom(32))
        # AES key for our Lottery CSPRNG
        f.write(os.urandom(16))

with open('app-secret.key', 'rb') as f:
    SECRET_KEY = f.read(32)
    LOTTERY_KEY = f.read(16)

app = Flask(__name__)
app.secret_key = SECRET_KEY

page = """
<!doctype html>
<html>
<head>
    <title>Fallmerayer Lottery!</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='pico.slim.min.css') }}">
    <meta charset="UTF-8">
</head>
<body>
<main class="container">
<header>
<h1><img src="/static/Fallmerayer.svg" style="height:0.8em; position:relative; top:-3px"> Lottery <span style="color: red; font-size: 0.7em; rotate: 30deg; display: inline-block">v2</span></h1>
</header>
<section>
Welcome to the Fallmerayer Lottery "6aus49 plus Superzahl!". It's like real Lottery except you can check whether your guesses were right or not without having to wait! How convenient!</br>
Though I suppose the prices might be a bit underwhelming...
</section>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <section>
    <article style="background-color: #18232c">
    <p>
    {% for message in messages %}
      {{ message }} </br>
    {% endfor %}
    </p>
    </article>
    </section>
  {% endif %}
{% endwith %}
<section>
Fill out your lottery ticket:</br>
</section>
<form action="/submitticket" method="post">
  <div class="grid">
  <input type="number" name="number1" min="1" max="49" value="1" required>
  <input type="number" name="number2" min="1" max="49" value="2" required>
  <input type="number" name="number3" min="1" max="49" value="3" required>
  <input type="number" name="number4" min="1" max="49" value="4" required>
  <input type="number" name="number5" min="1" max="49" value="5" required>
  <input type="number" name="number6" min="1" max="49" value="6" required>
  </div>
  <label for="superzahl">Superzahl:</label>
  <input type="number" name="superzahl" min="0" max="9" value="0" required></br></br>
  <button type="submit" {% if filled_out_ticket %} disabled {% endif %}>Submit</button>
</form>

<section>
Check if you are a winner:</br>
</section>
<form action="/checkdrawing">
  <button type="submit" {% if not filled_out_ticket%} disabled {% endif %}>Check</button>
</form>
</main>
</body>
</html>
"""


@app.route("/submitticket", methods=["POST"])
def submitticket():
    KEYS = ["number1", "number2", "number3", "number4", "number5", "number6", "superzahl"]
    if any([key not in request.form or int(request.form[key]) not in range(50) for key in KEYS]):
        flash("Invalid request: missing or invalid form parameters")
        return redirect("/")

    if "ticket" in session:
        flash("You have already filled out your ticket for this drawing!")
        return redirect("/")

    ticket = [int(request.form[key]) for key in KEYS]
    session["ticket"] = ticket
    flash("Your ticket was successfully filled out and submitted!")
    return redirect("/")


@app.route("/checkdrawing")
def checkdrawing():
    if "ticket" not in session:
        flash("You need to fill out your lottery ticket before checking the drawing!")
        return redirect("/")

    if "seed" not in session:
        nonce = os.urandom(8)
        ctr = 0
        session["seed"] = nonce + ctr.to_bytes(length=8, byteorder='big')

    # Utilize CSPRNG: AES "in CTR mode" with a secure key!
    nonce, ctr = session["seed"][:8], session["seed"][8:]
    aes = AES.new(LOTTERY_KEY, AES.MODE_ECB)
    rnd = aes.encrypt(nonce + ctr)

    # Generate lottery numbers 6aus49 plus Superzahl!
    lottery_numbers = [(x % 49) + 1 for x in rnd[:6]] + [rnd[6] % 10]

    if lottery_numbers == session["ticket"]:
        flag = subprocess.check_output(["/bin/flag", "3"]).decode()
        flash(f"Wow you're really lucky huh?? Here is your price: {flag}")
    else:
        flash("Sorry you aren't a winner today!")
    flash(f"Todays drawings are: {lottery_numbers}")
    flash("Alle Angaben wie immer ohne Gewähr.")
    
    # Increment the counter
    ctr = (int.from_bytes(ctr, byteorder='big') + 1).to_bytes(length=8, byteorder='big')

    # Update the seed
    session["seed"] = nonce + ctr

    del session["ticket"]
    return redirect("/")


# We decided custom session management might not be such a good idea... so let's use flasks secure default implementation!
@app.route("/")
def index():
    return render_template_string(page, filled_out_ticket="ticket" in session)

if __name__ == "__main__":
	app.run("0.0.0.0", 5003)
