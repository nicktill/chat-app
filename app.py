from flask import Flask, request, abort, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class userChatter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    repassword = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)


@app.route("/")
def default():
    return render_template("index.html")


# @app.route("/login/", methods=["GET", "POST"])
# def login_controller():


@app.route("/register/", methods=["GET", "POST"])
def register_controller():
    if request.method == 'POST':
        username_ = request.form['username']
        email_ = request.form['email']
        password_ = request.form['password']
        rePassword_ = request.form['rePassword']
        addUserInfo = userChatter(
            username=(username_),
            email=(email_),
            password=(password_),
            repassword=(rePassword_)
        )
        try:
            db.session.add(addUserInfo)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your information to database'
    else:
        return render_template('register.html')

    return redirect('/')

    # else:
    #     return redirect('/')


# @app.route("/profile/<username>")
# def profile(username=None):


# @app.route("/logout/")
# def unlogger():


# @app.route("/new_message/", methods=["POST"])
# def new_message():


# @app.route("/messages/")
# def messages():

if __name__ == "__main__":
    app.run(debug=True)
