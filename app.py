from ast import And
from urllib import response
from flask import Flask, request, abort, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'} 
db = SQLAlchemy(app)



class userChatter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

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
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = userChatter.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username  
            return redirect(url_for("profile", username=username))
        else:
            return render_template("loginPage.html", error="Invalid username or password")
    else:
        return render_template("loginPage.html")
 
app.route("/register/", methods=["GET", "POST"]) 
def register_controller():
    # Check if the request method is a POST and if so add to database
    if request.method == "POST":
        username_ = request.form["user"]
        email_ = request.form["email"]
        password_ = request.form["pass"]
        repassword_ = request.form["repass"]
        if password_ == repassword_:
            try:
                new_user = userChatter(username=username_, email=email_, password=password_)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("profile", username=username_))
            except:
                return "There was an issue adding your profile"
    else:
        return render_template("register.html")
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
