"""
Kavita Amin
12/3/2017
"""


from flask import Flask, render_template, redirect, flash, request
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "Secret"

@app.route('/')
def index(): 
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register(): 
    isError = False

    # no fields left empty
    if len(request.form["firstname"]) < 1: 
        flash("First Name is required.")
        isError = True
    if len(request.form["lastname"]) < 1: 
        flash("Last Name is required.")
        isError = True
    if len(request.form["email"]) < 1: 
        flash("Email is required.")
        isError = True
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")    
        isError = True    
    if len(request.form["password"]) < 9: 
        flash("Password is required and should be more than 8 characters.")
        isError = True
    if len(request.form["firstname"]) < 1: 
        flash("Please confirm your password.")
        isError = True

    # checking if name contains numbers
    if request.form["firstname"].isalpha() == False: 
        flash("First name should not contain any numbers.")
        isError = True
    if request.form["lastname"].isalpha() == False: 
        flash("Last name should not contain any numbers.")
        isError = True

    # password fields should match 
    if (request.form["password"]) != (request.form["password_confirm"]): 
        flash("Passwords must match.")
        isError = True

    if isError == True: 
        return redirect('/')
    else: 
        flash("Thanks for submitting your information.")
        return redirect('/')    


app.run(debug=True)
