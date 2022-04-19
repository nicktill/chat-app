from urllib import response
from flask import Flask, request, abort, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import tkinter
from tkinter import messagebox

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'} 
db = SQLAlchemy(app)


users = {"alice": "qwert", "bob": "asdfg", "charlie": "zxcvb"}

class userChatter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    repassword = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)

class chatInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chatMessage =  db.Column(db.String(150), nullable=False)
    __bind_key__ = 'chat' 



@app.route("/", methods=["GET", "POST"])
def default():
    print("redirecting to login_controller for the first time")
    return redirect(url_for("login_controller"))
 

@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    # grab userID from database as follows
    # usernameID =  userChatter.query.order_by(userChatter.username).all()
    if request.method == "POST":
        print("post request")
    print(request.form)	
    if "username" in request.form and "password" in request.form:
        print("checking if the user is one of our clients")	
        # if request.form["username"] in session && request.form["password"] in session:
        if request.form["username"] in users:
                # return render_template("chat_page.html", usernameID={usernameID})
                return render_template("chat_page.html")
        else:
                print("username is incorrect")
                abort(401)
    else:
        return render_template('loginPage.html')


@app.route("/register/", methods=["GET", "POST"])
def register_controller():
    #if user is making a register post request (trying to register)
    if request.method == 'POST': 
        username_ = request.form['username']
        email_ = request.form['email']
        password_ = request.form['password']
        rePassword_ = request.form['rePassword']
        if password_ == rePassword_:
            addUserInfo = userChatter(
                username=(username_),
                email=(email_),
                password=(password_),
                repassword=(rePassword_)
            )
        # else:
        #     messagebox.showinfo("Passwords do not match:", "Passwodrs must match in order to")
        #     return redirect("/register/")
       
        try:
            db.session.add(addUserInfo)
            db.session.commit()
            return redirect('/login/')
        except:
            return 'There was an issue adding your information to database'
    
    #if user is trying to get to register page (clicked register button)
    else:
        return render_template('register.html')

@app.route("/profile/")
@app.route("/profile/<username>")
def profile(username=None):
	if not username:
		# if no profile specified, either:
		#	* direct logged in users to their profile
		#	* direct unlogged in users to the login page
		if "username" in session:
			return redirect(url_for("profile", username=session["username"]))
		else:
			return redirect(url_for("login_controller"))
			
	elif username in users:
		# if specified, check to handle users looking up their own profile
		if "username" in session and session["username"] == username:
			return render_template("curProfile.html")
		else:
			return render_template("otherProfile.html", name=username)
			
	else:
		# cant find profile
		abort(404)

@app.route("/logout/")
def unlogger():
	# if logged in, log out, otherwise offer to log in
	if "username" in session:
		# note, here were calling the .clear() method for the python dictionary builtin
		session.clear()
		return render_template("logoutPage.html")
	else:
		return redirect(url_for("login_controller"))


# @app.route("/new_message/", methods=["POST"])
# def new_message():


# @app.route("/messages/")
# def messages():

if __name__ == "__main__":
    app.run(debug=True)
