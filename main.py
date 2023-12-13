import json
import os
from datetime import datetime

import requests
from flask import Flask, render_template, redirect, url_for, flash, abort, request, current_app, jsonify, make_response, \
    Response


from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.utils import secure_filename
import uuid

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table
    user = User.query.get(int(user_id))
    if user:
        return user
    # If not, check if user is in free_user table

    # If user is not in either table, return None
    return None

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():


    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
        email = db.Column(db.String(100))
        role = db.Column(db.String(100), default="user")
        pay = db.Column(db.Boolean(), default=False)
        message = db.Column(db.String(1000))
        starting_day = db.Column(db.DateTime)
        due_Date = db.Column(db.DateTime)
        delegate = db.Column(db.DateTime)
        weight=db.Column(db.String(100))
        tall=db.Column(db.String(100))
        age=db.Column(db.String(100))
        health=db.Column(db.String(100))
        numbers=db.Column(db.String(100))
        member=db.Column(db.String(100))
        adress=db.Column(db.String(100))
        gender=db.Column(db.String(100))
    db.create_all()


class MyModelView(ModelView):
    def is_accessible(self):
            return True

admin = Admin(app)
admin.add_view(MyModelView(User, db.session))
@app.route("/")
def start():
    return render_template("index.html")
@app.route("/r",methods=["GET","POST"])

def r():
    if request.method=="POST":
        first_name = request.form.get('First Name')
        last_name = request.form.get('Last Name')
        gender = request.form.get('Gender')
        dob_day = request.form.get('dob_day')  # You need to add names to the DOB fields in the HTML
        dob_month = request.form.get('dob_month')
        dob_year = request.form.get('dob_year')
        username = request.form.get('Username')
        password = request.form.get('Password')
        email = request.form.get('Email')
        phone = request.form.get('Phone')
        address = request.form.get('Address')
        weight = request.form.get('weight')
        tall = request.form.get('tall')
        age = request.form.get('Age')
        diseases = request.form.get('diseases')
        payment_option = request.form.get('Payment')
        new_user=User(
        phone=phone,name=first_name,email=email,password=password,weight=weight,tall=tall,age=age,health=diseases,member=payment_option,gender=gender,adress=address,
                starting_day=datetime.today()
        )
        db.session.add(new_user)
        db.session.commit()
        return "user enterd "


    return  render_template("register.html")
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)