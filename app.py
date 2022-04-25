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
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
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
            return redirect(url_for("profile", username=username))
        else:
            return render_template("loginPage.html", error="Invalid username or password")
    else:
        return render_template("loginPage.html")
 
@app.route("/register/", methods=["GET", "POST"]) 
def register_controller():
    # Check if the request method is a POST and if so add to database
    if request.method == "POST":
        user_username = request.form["username"]
        user_email = request.form["email"]
        user_password = request.form["password"]
        user_repass = request.form["repassword"]
        if user_password == user_repass:
            try:
                new_user = userChatter(username=user_username, email=user_email, password=user_password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("profile", username=user_username))
            except:
                return "There was an issue adding your profile"
    else:
        return render_template("register.html")
 
 
# @app.route("/login/", methods=["GET", "POST"])
# def login_controller():
#     if request.method == "POST":
#         username = request.form['username']
#         password = request.form['password']
#         user = userChatter.query.filter_by(username=username).first()
#         if user and user.password == password:
#             session['username'] = username  
#             return redirect(url_for("profile", username=username))
#         else:
#             return render_template("loginPage.html", error="Invalid username or password")
#     else:
#         return render_template("loginPage.html")
 
# @app.route("/register/", methods=["GET", "POST"]) 
# def register_controller():
#     # Check if the request method is a POST and if so add to database
#     if request.method == "POST":
#         username_ = request.form["username"]
#         email_ = request.form["email"]
#         password_ = request.form["password"]
#         repassword_ = request.form["repassword"]
#         if password_ == repassword_:
#             try:
#                 userChatterInfo = userChatter(username=username_, email=email_, password=password_)
#                 db.session.add(userChatterInfo)
#                 db.session.commit()
#                 return redirect(url_for("profile", username=username_))
#             except:
#                 return "There was an issue adding your profile"
#     else:
#         return render_template("register.html")

@app.route("/profile/<username>")
def profile(username=None):
    if username:
        user = userChatter.query.filter_by(username=username).first()
        chats = chatInfo.query.order_by(chatInfo.date_created.desc()).all()
        if user:
            return render_template("chat_page.html", user=user, chatMessage=chats)
        else:
            return "specified user not found"


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
    app.secret_key = "super secret key"
    app.run(debug=True)
