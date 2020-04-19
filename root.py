from flask import Flask, render_template, request,session, redirect, url_for, escape, request,flash,get_flashed_messages
from flask import Flask, render_template, flash
from flask import Flask, redirect, url_for, request
import werkzeug
from werkzeug.datastructures import ImmutableMultiDict
import pprint
import pymysql
import requests
import pprint
import re
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
global username
app = Flask(__name__)
app.secret_key = "secret_key"

@app.route("/")
def root():
   return render_template("login.html")

@app.route('/login.html',methods = ['POST', 'GET'])
def index():
   global username
   loginSuccess = False
   database = pymysql.connect("localhost", "root", "root", "test")
   sql_to_select = "select * from tbl_auth"
   cursor = database.cursor()
   cursor.execute(sql_to_select)
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      for credential in cursor.fetchall():
         if credential[0] == username and credential[1] == password:
            loginSuccess = True

   if(loginSuccess):
      print("Login Success True")
      session['username'] = username
      return redirect(url_for('home',username=username))
   else:
      print("Login Success False")
      flash("Entered Credentials Are Wrong")
      return redirect(url_for('logout'))

@app.route('/logout')
def logout():
   if 'username' in session:
      session.pop('username', None)
   return redirect(url_for('root'))

@app.route('/home')
def home():
   global username
   if 'username' in session:
      return render_template("home.html", username=username)
   else:
      return "Not Authorized"

@app.route('/about')
def about():
   return render_template("about.html")

@app.route('/contact')
def contact():
   if 'username' in session:
      return render_template("contact.html")
   else:
      return "Not Authorized"