from types import MemberDescriptorType
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import cs50 
from cs50 import SQL
from flask import g
import sqlalchemy

app = Flask(__name__)
app.secret_key = 'super secret key'

db = SQL("sqlite:///user.db")
#database = sqlite3.connect("user.db",check_same_thread=False)  # part to check
#db=database.cursor()    
#db.execute("create table users( email_id VARCHAR(20) , hash VARCHAR(30) , mobile_no VARCHAR(10))")

#db.execute(" create table VACCINE(fname varchar(20),lname varchar(20),age int ,mobile_no varchar(20),email varchar(20),country varchar(20),vaccinestatus varchar(20),vaccinetype varchar(20))")
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
                return apology("Enter valid username/password",400 )
            # Remember which user has logged in
            session["user_id"] = rows[0]["email_id"]
            
            if rows[0]["email_id"]=="admin@314ecorp.com":
                return redirect("/admin")

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

@app.route("/admin",methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form.get("sub"):
            redirect("/admin")
    else:
     member = db.execute("SELECT * FROM VACCINE ")
     return render_template("admin.html", mem=member)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        mobile = request.form.get("mobile_no")
        
        if len(mobile)!=10:
            return apology("Enter correct mobile number",400)

        email = str(request.form.get("Email"))
        
        
        listofemail= email.split("@")
        
        if listofemail[1] != "314ecorp.com":
            return apology("Enter the official mail id",400)
        p1=request.form.get("password")
        p2=request.form.get("confirm_password")
        if p1!=p2 :
            return apology("password mismatch",403)
 

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
        email=request.form.get("email")
        age=request.form.get("age")
        mobile_no=request.form.get("mobile-number")
        country=request.form.get("country")
        vaccine_status=request.form.get("Vaccinestatus")
        vaccine_administered=request.form.get("vaccine")
        print(firstname,lastname,age,mobile_no,email,country,vaccine_status,vaccine_administered)
        db.execute("INSERT INTO VACCINE(fname,lname,age,mobile_no,email,country,vaccinestatus,vaccinetype) VALUES(?,?,?,?,?,?,?,?)",firstname,lastname,age,mobile_no
                ,email,country,vaccine_status,vaccine_administered)

        if vaccine_status=="0-dose":
            return redirect("https://www.cowin.gov.in/home")
        elif vaccine_status=="1-dose":
             return redirect("https://www.cowin.gov.in/home")
        else:
             return  redirect("https://www.amazon.in/gift-card-store/b?ie=UTF8&node=3704982031")
        
        
     else:
       return(render_template("form.html")) 




  # function for returning apology message 
def apology(message,error_id):
#    return("Error"+" "+message)
     return(render_template("apology.html",top=message ))


@app.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run()
