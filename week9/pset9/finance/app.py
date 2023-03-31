import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    user_id = session["user_id"]

    user_stock_data = db.execute("SELECT symbol AS stock, quantity AS shares FROM user_stocks WHERE user_id = ?", user_id)

    for stock in user_stock_data:
        quote = lookup(stock["stock"])
        # Adding current_price key to stock dictionary
        stock_current_price_unrounded = quote["price"]
        stock_current_price_rounded_str = f"{stock_current_price_unrounded:.2f}"
        stock["current_price"] = stock_current_price_rounded_str
        # Adding total_value key to stock dictionary
        stock_total_value_unrounded = stock["shares"] * float(stock["current_price"])
        stock_total_value_rounded_str = f"{stock_total_value_unrounded:.2f}"
        stock["total_value"] = stock_total_value_rounded_str


    # Calculate user cash total
    user_cash_total_as_list = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    user_cash_total_unrounded = user_cash_total_as_list[0]["cash"]
    user_cash_total_rounded_str = f"{user_cash_total_unrounded:.2f}"

    # Calculate user total stock value
    user_total_stock_value_unrounded = 0.0
    for stock in user_stock_data:
        user_total_stock_value_unrounded = user_total_stock_value_unrounded + float(stock["total_value"])

    # Calculate user total value by adding cash total and total stock value
    user_total_value_unrounded = user_total_stock_value_unrounded + user_cash_total_unrounded
    user_total_value_rounded_str = f"{user_total_value_unrounded:.2f}"

    return render_template("index.html", user_stock_data=user_stock_data, cash_total=user_cash_total_rounded_str, total_value=user_total_value_rounded_str)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    user = session["user_id"]

    if request.method == "POST":
        submitted_symbol = request.form.get("symbol")
        submitted_quantity = request.form.get("shares")

        if not submitted_quantity:
            return apology("No quantity submitted")
        elif not submitted_quantity.isnumeric():
            return apology("Please enter a number for quantity of shares")
        elif not submitted_quantity.isdigit():
            return apology("Please enter a whole number for quantity of shares")

        quantity = int(submitted_quantity)
        quote = lookup(submitted_symbol)

        if not submitted_symbol:
            return apology("No symbol submitted")
        elif quote is None:
            return apology("Symbol does not exist")
        elif quantity < 1:
            return apology("Quantity of shares must be at least 1")
        else:
            user_cash_as_list = db.execute("SELECT cash FROM users WHERE id = ?", user)
            user_cash = float(user_cash_as_list[0]["cash"])
            total_price_of_purchase_unrounded = float(quantity) * quote["price"]
            total_price_of_purchase_rounded_str = f"{total_price_of_purchase_unrounded:.2f}"
            if float(total_price_of_purchase_rounded_str) > user_cash:
                return apology("Sorry, but you don't have enough cash to make this purchase")
            else:
                now = datetime.now()
                year = int(now.strftime("%Y"))
                month = int(now.strftime("%m"))
                day = int(now.strftime("%d"))
                hour = int(now.strftime("%H"))
                minute = int(now.strftime("%M"))

                price_in_cents = int(float(total_price_of_purchase_rounded_str) * 100)

                # Inserting data into transactions table
                db.execute("INSERT INTO transactions (type, symbol, price_in_cents, quantity, year, month, day, hour, minute, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", "purchase", quote["symbol"], price_in_cents, quantity, year, month, day, hour, minute, user)


                # Grabbing transcation_id of most recent purchase to add into purchases table
                last_row_of_transactions_table = db.execute("SELECT * FROM transactions WHERE id = (SELECT max(id) FROM transactions)")
                transaction_id = last_row_of_transactions_table[0]["id"]
                # Inserting data into purchases table
                db.execute("INSERT INTO purchases (symbol, price_of_purchase_in_cents, quantity, year, month, day, hour, minute, transaction_id, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", quote["symbol"], price_in_cents, quantity, year, month, day, hour, minute, transaction_id, user)


                # Update user's stock data in user_stocks table
                all_user_stock_data = db.execute("SELECT * FROM user_stocks WHERE user_id = ?", user)
                user_owns_this_companys_stocks = False
                # Loop through user's stocks to check if user already owns this company's stocks
                # If he does, then update the quantity of that stock
                # If he doesn't, insert a new row for that stock for that user
                for stock in all_user_stock_data:
                    if not user_owns_this_companys_stocks:
                        if stock["symbol"] == quote["symbol"]:
                            user_owns_this_companys_stocks = True

                            # Getting the # of stocks that the user already owned before buying
                            pre_purchase_quantity_as_list = db.execute("SELECT quantity FROM user_stocks WHERE user_id = ? AND symbol = ?", user, stock["symbol"])
                            pre_purchase_quantity = int(pre_purchase_quantity_as_list[0]["quantity"])

                            db.execute("UPDATE user_stocks SET quantity = ? WHERE user_id = ? AND symbol = ?", pre_purchase_quantity + quantity, user, stock["symbol"])

                if not user_owns_this_companys_stocks:
                    db.execute("INSERT INTO user_stocks (user_id, symbol, quantity) VALUES (?, ?, ?)", user, quote["symbol"], quantity)



                # Update user cash total
                user_cash = user_cash - float(total_price_of_purchase_rounded_str)
                db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash, user)

                return redirect("/")


    elif request.method == "GET":
        return render_template("buy.html")


@app.route("/change", methods=["GET", "POST"])
def change_password():
    """ Change user password """

    user = session["user_id"]
    if request.method == "POST":
        submitted_current_password = request.form.get("current_password")
        submitted_new_password = request.form.get("new_password")
        submitted_new_password_confirmation = request.form.get("new_password_confirmation")

        current_password_hash_as_list = db.execute("SELECT hash FROM users WHERE id = ?", user)
        current_password_hash = current_password_hash_as_list[0]["hash"]

        if not submitted_current_password:
            return apology("Current password not entered")
        elif not submitted_new_password:
            return apology("New password not entered")
        elif not submitted_new_password_confirmation:
            return apology("New password confirmation not entered")
        elif not check_password_hash(current_password_hash, submitted_current_password):
            return apology("Sorry, current password entered is incorrect")
        elif not submitted_new_password == submitted_new_password_confirmation:
            return apology("Same new password must be entered two times")
        else:
            new_password_hash = generate_password_hash(submitted_new_password, method='pbkdf2:sha256', salt_length=8)
            db.execute("UPDATE users SET hash = ? WHERE id = ?", new_password_hash, user)

            flash("Password successfully changed!")
            return redirect("/")

    elif request.method == "GET":
        return render_template("change.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user = session["user_id"]

    all_transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user)

    # Adding price_in_dollars key to all transaction dicts to make it easier to
    # render price in terms of dollars on history page.
    for transaction in all_transactions:
        price_in_dollars_unrounded = float(transaction["price_in_cents"]) / float(100);
        price_in_dollars_rounded_str = f"{price_in_dollars_unrounded:.2f}"
        transaction["price_in_dollars"] = float(price_in_dollars_rounded_str)

    return render_template("history.html", transactions=all_transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
        submitted_symbol = request.form.get("symbol")
        # If user didn't input anything
        if not submitted_symbol:
            return apology("No quote submitted")

        quote = lookup(submitted_symbol)

        # If lookup was successful, e.g. if submitted quote exists
        if quote is not None:
            name = quote["name"]
            price = quote["price"]
            price_rounded_str = f"{price:.2f}"
            symbol = quote["symbol"]
            return render_template("quoted.html", name=name, price=price_rounded_str, symbol=symbol)
        else:
            return apology("Submitted quote does not exist")

    elif request.method == "GET":
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        existing_users = db.execute("SELECT * FROM users")
        existing_usernames = []
        for user in existing_users:
            existing_usernames.append(user["username"])

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Username validation

        # If input for username was left blank
        if not username:
            return apology("Username left blank")
        # If username already exists
        elif username in existing_usernames:
            return apology("Username already exists")

        # Password validation

        elif not password:
            return apology("Password not entered")
        elif not confirmation:
            return apology("Password confirmation not entered")
        elif password != confirmation:
            return apology("Passwords do not match")
        else:
            password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)
            return redirect("/login")

    elif request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user = session["user_id"]

    if request.method == "POST":
        user_stock_dicts = db.execute("SELECT symbol, quantity FROM user_stocks WHERE user_id = ?", user)

        user_stocks = []
        user_stock_quantities = []

        for stock in user_stock_dicts:
            user_stocks.append(stock["symbol"])
            user_stock_quantities.append(stock["quantity"])

        selected_symbol = request.form.get("symbol")
        submitted_quantity = request.form.get("shares")


        if not selected_symbol:
            return apology("No stock selected")
        elif selected_symbol not in user_stocks:
            return apology("Sorry, you don't own any shares of this stock")
        elif not submitted_quantity.isnumeric():
            return apology("Please enter a number for quantity of shares")
        elif not submitted_quantity.isdigit():
            return apology("Please enter a whole number for quantity of shares")
        else:
            quantity = int(submitted_quantity)
            quote = lookup(selected_symbol)

            if quote is None:
                return apology("Submitted stock does not exist")
            elif quantity > user_stock_quantities[user_stocks.index(selected_symbol)]:
                return apology("You do not own this many shares of the selected stock.")
            elif quantity < 1:
                return apology("Quantity of shares must be at least 1")
            else:
                now = datetime.now()
                year = int(now.strftime("%Y"))
                month = int(now.strftime("%m"))
                day = int(now.strftime("%d"))
                hour = int(now.strftime("%H"))
                minute = int(now.strftime("%M"))


                user_cash_as_list = db.execute("SELECT cash FROM users WHERE id = ?", user)
                user_cash = float(user_cash_as_list[0]["cash"])

                total_price_of_sale_unrounded = float(quantity) * quote["price"]
                total_price_of_sale_rounded_str = f"{total_price_of_sale_unrounded:.2f}"

                price_in_cents = int(float(total_price_of_sale_rounded_str) * 100)

                # Inserting data into transactions table
                db.execute("INSERT INTO transactions (type, symbol, price_in_cents, quantity, year, month, day, hour, minute, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", "sale", quote["symbol"], price_in_cents, quantity, year, month, day, hour, minute, user)

                # Grabbing transcation_id of most recent sale to add into sales table
                last_row_of_transactions_table = db.execute("SELECT * FROM transactions WHERE id = (SELECT max(id) FROM transactions)")
                transaction_id = last_row_of_transactions_table[0]["id"]
                # Inserting data into sales table
                db.execute("INSERT INTO sales (symbol, price_of_sale_in_cents, quantity, year, month, day, hour, minute, transaction_id, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", quote["symbol"], price_in_cents, quantity, year, month, day, hour, minute, transaction_id, user)

                # Update user's stock data in user_stocks table
                all_user_stock_data = db.execute("SELECT * FROM user_stocks WHERE user_id = ?", user)
                user_stock_data_updated = False

                for stock in all_user_stock_data:
                    if not user_stock_data_updated:
                        if stock["symbol"] == quote["symbol"]:
                            pre_sale_quantity_as_list = db.execute("SELECT quantity FROM user_stocks WHERE user_id = ? AND symbol = ?", user, stock["symbol"])
                            pre_sale_quantity = int(pre_sale_quantity_as_list[0]["quantity"])

                            if pre_sale_quantity - quantity == 0:
                                db.execute("DELETE FROM user_stocks WHERE user_id = ? AND symbol = ?", user, quote["symbol"])
                            else:
                                db.execute("UPDATE user_stocks SET quantity = ? WHERE user_id = ? AND symbol = ?", pre_sale_quantity - quantity, user, quote["symbol"])

                            user_stock_data_updated = True


                # Update user cash total
                user_cash = user_cash + float(total_price_of_sale_rounded_str)
                db.execute("UPDATE users SET cash = ? WHERE id = ?", user_cash, user)

                return redirect("/")

    elif request.method == "GET":
        user_stocks = db.execute("SELECT symbol FROM user_stocks WHERE user_id = ?", user)
        return render_template("sell.html", user_stocks=user_stocks)