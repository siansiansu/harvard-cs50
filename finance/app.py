import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    username = session["username"]

    if request.method == "POST":
        funds = request.form.get("funds")
        funds = float(funds)

        if not funds or funds < 0:
            return apology("must transfer greater than 0 funds", 400)

        cash = db.execute(
            "SELECT cash from users WHERE username = :username", username=username
        )
        cash = cash[0]["cash"]

        cash += funds
        db.execute(
            "UPDATE users SET cash=:cash WHERE username=:username",
            cash=cash,
            username=username,
        )

        flash("Successfully added funds!")
        return redirect("/")

    rows = db.execute(
        "SELECT symbol, name, SUM(shares) AS totalshares from orders WHERE username = :username GROUP BY name HAVING totalshares > 0",
        username=username,
    )
    cash = db.execute(
        "SELECT cash from users WHERE username = :username", username=username
    )
    cash = cash[0]["cash"]
    balance = cash

    for row in rows:
        symbol = row["symbol"]
        temp = lookup(symbol)
        row["price"] = temp["price"]
        row["total"] = row["price"] * row["totalshares"]
        balance += row["total"]
    return render_template("index.html", rows=rows, cash=cash, balance=balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        username = session["username"]
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol or not shares:
            return apology("must fill in symbol and shares", 400)

        if symbol == "":
            return apology("symbol cannot be a empty string", 400)

        if shares.isalpha():
            return apology("symbol cannot be a non-numeric", 400)

        if "." in shares:
            return apology("symbol cannot be a fractional", 400)

        shares = int(float(shares))

        if shares < 0:
            return apology("number of shares must be more than 0", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("stock not found")

        price = quote["price"] * shares
        rows = db.execute(
            "SELECT cash from users WHERE username = :username", username=username
        )
        current_cash = rows[0]["cash"]
        balance = current_cash - price
        if price > current_cash:
            return apoloy("the price of stock is greater than your cash.", 400)

        db.execute(
            "INSERT INTO orders (username, symbol, name, shares, price) VALUES(?,?,?,?,?)",
            username,
            quote["symbol"],
            quote["name"],
            shares,
            quote["price"],
        )
        db.execute(
            "UPDATE users SET cash=:balance WHERE username=:username",
            balance=balance,
            username=username,
        )
        flash("Bought!")
        return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    username = session["username"]
    rows = db.execute(
        "SELECT symbol, shares, price, transacted from orders WHERE username = :username",
        username=username,
    )
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = username

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must input stock symbol", 400)
        quote = lookup(symbol)
        if not quote:
            return apology("stock not found", 400)
        return render_template("quoted.html", quote=quote)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username or not password or not confirmation:
            return apology("Please fill in the fields", 400)

        rows = db.execute(
            "SELECT * FROM users WHERE username = :username", username=username
        )

        if len(rows) >= 1:
            return apology("Username already exists!", 400)

        if len(password) < 8:
            return apology("Make sure your password is at lest 8 letters.", 400)

        if not re.search("[a-z]", password):
            return apology("Make sure your password has a lowercase letter in it.", 400)

        if not re.search("[A-Z]", password):
            return apology("Make sure your password has a capital letter in it.", 400)

        if not re.search("[0-9]", password):
            return apology("Make sure your password has a number in it.", 400)

        if re.search("\s", password):
            return apology(
                "Make sure your password cannot contain white spaces in it.", 400
            )

        if confirmation != password:
            return apology("Password does not the same!", 400)

        hashed_password = generate_password_hash(password)
        rows = db.execute(
            "INSERT INTO users (username, hash) VALUES(?,?)", username, hashed_password
        )
        flash("Account created!")
        return redirect("/")
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        username = session["username"]
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # if not symbol or not shares:
        #     return apology("must fill in symbol and shares", 400)

        if shares.isalpha():
            return apology("symbol cannot be a non-numeric", 400)

        if "." in shares:
            return apology("symbol cannot be a fractional", 400)

        shares = int(float(shares))

        if shares < 0:
            return apology("shares must be greater than 0", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("stock not found", 400)

        total = quote["price"] * shares
        cash = db.execute(
            "SELECT cash from users WHERE username = :username", username=username
        )
        cash = cash[0]["cash"]
        current_shares = db.execute(
            "SELECT SUM(shares) AS totalshares from orders WHERE symbol = :symbol AND username = :username GROUP BY name",
            symbol=symbol,
            username=username,
        )
        current_shares = current_shares[0]["totalshares"]

        if current_shares < shares:
            return apology("shares are insufficient", 400)

        db.execute(
            "INSERT INTO orders (username, symbol, name, shares, price) VALUES(?,?,?,?,?)",
            username,
            quote["symbol"],
            quote["name"],
            -1 * shares,
            quote["price"],
        )
        db.execute(
            "UPDATE users SET cash=:balance WHERE username=:username",
            balance=cash + total,
            username=username,
        )

        flash("Sold!")
        return redirect("/")
    symbols = db.execute("SELECT DISTINCT(symbol) from orders")
    return render_template("sell.html", symbols=symbols)
