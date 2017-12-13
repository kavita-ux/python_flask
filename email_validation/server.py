from flask import Flask, redirect, request, render_template, flash
from mysqlconnection import MySQLConnector
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = MySQLConnector(app,'emaildb')
app.secret_key = "Secret"

@app.route('/')
def index(): 
    return render_template("index.html")

@app.route('/process', methods=["POST"])
def process(): 
    if len(request.form['email']) < 1: 
        flash("Email is required.")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Please enter a valid email.")   
    email = request.form['email']
    email_query = "SELECT * FROM emails where emails.address = :email LIMIT 1"
    query_data =  {'email': email}
    email_address = mysql.query_db(email_query, query_data)
    if len(email_address) < 1: 
        flash("Email not found.")
        return redirect('/')
    for address in email_address: 
        if (address['address'] == email): 
            return render_template("success.html", email = email_address, entered = email)


app.run(debug=True)

