''' 
Kavita Amin
12/7/2017
Assignment: Login and Registration using Flask and MySQL 
'''

from flask import Flask, render_template, redirect, flash, session, request 
import re 
from mysqlconnection import MySQLConnector 
import md5 
import os, binascii

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
mysql = MySQLConnector(app, 'users_profiles_db')
app.secret_key = "secret_key"

@app.route('/')
def index(): 
    return render_template("index.html")

@app.route('/login')
def login(): 
    return render_template("login.html")

@app.route('/login_process', methods=["POST"])
def login_process(): 
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    isError = False
    errors = []
    isInDatabase = False

    # data format validation
    if not EMAIL_REGEX.match(session['email']):
        isError = True
        errors.append("Your email cannot be blank, and should look like example@example.com")

    if len(session['password']) < 8: 
        isError = True
        errors.append("Your password should be at least 8 characters")

    # check if provided email is in database
    query = "SELECT email FROM users WHERE email = '{}'".format(session['email'])
    resultSet = mysql.query_db(query)
    if len(resultSet) < 1: 
        isError = True
        errors.append("Email not found.")
    for result in resultSet: 
        if result['email'] == session['email']: 
            isInDatabase = True

    # if email is in database, check if password matches
    if isInDatabase == True:
        query = "SELECT hashed_password, salt FROM users WHERE email = '{}' LIMIT 1".format(session['email'])
        resultSet = mysql.query_db(query)
        result = resultSet[0]
        print "hashed pw: ", result['hashed_password']
        print "salt: ", result['salt']

        encrypted_password = md5.new(session['password'] + result['salt']).hexdigest()
        print encrypted_password

        if result['hashed_password'] == encrypted_password:
            return redirect('/success')
        else: 
            isError = True
            errors.append("Password does not match.")

    #  flash errors if any form fields are invalid
    if isError == True: 
        for error in errors: 
            flash(error)
        return redirect('/login')



@app.route('/registration')
def registration(): 
    return render_template("registration.html")

@app.route('/process_registration', methods=["POST"])
def process_registration(): 
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    confirmed_password = request.form['confirm_password']
    isError = False
    errors = []

    # validating form fields
    if len(session['first_name']) < 2 or len(session['last_name']) < 2: 
        isError = True
        errors.append("Your first and last name must be at least 2 characters long")
    if (session['first_name'].isalpha == False): 
        isError = True
        errors.append("Your first name should be letters only")
    if (session['last_name'].isalpha == False): 
        isError = True
        errors.append("Your last name should be letters only")
    if not EMAIL_REGEX.match(session['email']):
        isError = True
        errors.append("Your email format should look like example@example.com")
    if len(session['password']) < 8: 
        isError = True
        errors.append("Your password should be at least 8 characters")
    if (session['password'] != confirmed_password): 
        isError = True
        errors.append("Your passwords do not match")
    
    # flash errors if any form fields are invalid
    if isError == True: 
        for error in errors: 
            flash(error)
        return redirect('/registration')
    else: 
        salt = binascii.b2a_hex(os.urandom(15))
        session['password'] = md5.new(session['password'] + salt).hexdigest()

        # insert values into DB
        query = "INSERT INTO users (first_name, last_name, email, hashed_password, salt) VALUES ('{}','{}','{}','{}','{}')".format(session['first_name'], session['last_name'], session['email'], session['password'], salt)
        mysql.query_db(query)
        return redirect('/success')

@app.route('/success')
def success():
    query = "SELECT first_name FROM users WHERE email='{}' LIMIT 1".format(session['email'])
    resultSet = mysql.query_db(query)

    if len(resultSet) < 1: 
        return redirect('/')
    else: 
        result = resultSet[0]

    return render_template("success.html", username = result['first_name'])  


app.run(debug=True)
