from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from flask import g

app = Flask(__name__)

db = sqlite3.connect("user.db")  # part to check

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    print('Hello World part 1')
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("Email Id"):
            print(request.form.get("Email Id"))
            return apology("must provide Email id", 403)   # add the necessary page required

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)    # add the necessary page required

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email id = :email id",
                          username=request.form.get("Email Id"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)   # add the necessary page required

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        
        if not request.form.get("username"):
            return apology("provide username", 400)

        elif not request.form.get("password"):
            return apology("password", 400)
            
        
        mobile = request.form.get("mobile_number")
        
        if len(mobile)!=10:
            return apology("Enter correct mobile number",400)

        email = request.form.get("username")
        
        listofemail= email.split("@")
        
        if listofemail[1] != "314ecorp.com":
            return apology("Enter the official mail id",400)
 

        hash = generate_password_hash(request.form.get("password"))
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"),
                            hash=hash)
        if not result:
            return apology("email already exists", 400)

        session["user_id"] = result
        """Success message"""
        flash('Registered! Sign in using the same email id')
        return redirect("login.html")     #redirect to login page
    else:
        return render_template('login.html')







@app.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run()
