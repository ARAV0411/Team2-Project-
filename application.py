from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
#import sqlite3
import cs50 
from cs50 import SQL
from flask import g

app = Flask(__name__)
app.secret_key = 'super secret key'

#database = sqlite3.connect("user.db",check_same_thread=False)  # part to check
#db=database.cursor()    
#db.execute("create table users( email_id VARCHAR(20) , hash VARCHAR(30) , mobile_no VARCHAR(10))")
db = SQL("sqlite:///user.db")
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":        
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE email_id = ?",request.form.get("Email_Id"))
                        # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
                return apology("Enter valid username/password")
            # Remember which user has logged in
            session["user_id"] = rows[0]["email_id"]

            # Redirect user to home page
            return redirect("/form")
            
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

        mobile = request.form.get("mobile_no")
        
        if len(mobile)!=10:
            return apology("Enter correct mobile number",400)

        email = str(request.form.get("Email"))
        print(email)
        
        listofemail= email.split("@")
        
        if listofemail[1] != "314ecorp.com":
            return apology("Enter the official mail id",400)
 

        password = generate_password_hash(request.form.get("password"))
        result = db.execute("INSERT INTO users(email_id,hash,mobile_no) VALUES(?,?,?)",
                          email,password,mobile)
#        result = db.execute("INSERT INTO users(email_id) VALUES(?)",
#                           (email))
        if not result:
            return apology("email already exists", 400)

        session["user_id"] = result
        """Success message"""
        flash('Registered! Sign in using the same email id')
        return redirect("/login")     #redirect to login page
    else:
        return render_template("login.html")

@app.route("/form",method=["Get","Post"])
def form():
     if request.method == "POST":
        "function for checking vaccinate"
        firstname=request.form.get("fname")
        lastname=request.form.get("lname")
        age=request.form.get("age")
        mobile_no=request.form.get("mobile_no")
        email=request.form.get("email")
        country=request.form.get("country")
        vaccine_status=request.form.get("vaccine-status")
        vaccine_administered=request.form.get("vaccine-type")
        db.execute()

        if vaccine_status=="Yet to be vaccinated":
            "do"
        elif vaccine_status=="1st dose done":
            "do"
        else:
            "do"
        
        
     else:
         return(render_template("form.html"))




# function for returning apology message 
def apology(message,error_id):
    return("Error"+str(error_id)+message)


@app.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run()
