'''
Christian Alexa
12/6/2017
Assignment - Email Validation

Description:
The context is a sign up form.
If no email exists in the database, add it to the database.
If the email already exists or if there are validation errors, 
flash them to the user.
'''

from flask import Flask, render_template, flash, request, redirect
import re
from mysqlconnection import MySQLConnector

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
mysql = MySQLConnector(app, 'emailsdb')

app.secret_key = "secret_key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['post'])
def succes():

    isError = False
    isInDatabase = False

    # check if field is blank 
    if len(request.form['email']) < 1:
        flash ("*Email must not be empty.*")
        isError = True
    
    # check for regex email pattern
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("*Invalid email pattern.*")
        isError = True

    # make query and test if retrieving resultset
    query = "SELECT email, created_at FROM emails"
    data = {
        'email' : request.form['email']
    }
    resultSet = mysql.query_db(query, data)
    print "Result Set:", resultSet

    # check if exists in DB
    # iterate through the resultSet, which is a list of dictionaries
    for dictionary in resultSet:
        # check if email address is present as a value of a key
        if (dictionary['email'] == request.form['email']):
            print "email exists in database"
            flash ("*Email already exists in database*")
            isError = True  
            isInDatabase = True
   
    # if the email doesn't exist, we need to insert it into the database
    if isInDatabase == False:
        query = "INSERT INTO emails (email, created_at) VALUES ('{}', NOW())".format(request.form['email'])
        mysql.query_db(query)
        print "email inserted into database" # check in MySQL that it actually inserted

    query = "SELECT * FROM emails"
    finalResultSet = mysql.query_db(query)

    if isError == True:
        return redirect('/')
    else:
        return render_template('success.html', email = request.form['email'], finalResultSet = finalResultSet )

app.run(debug=True)