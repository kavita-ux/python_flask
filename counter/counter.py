'''
Kavita Amin
11/26/2017
'''


from flask import Flask, render_template, session
app = Flask(__name__)
app.secret_key = 'SecretKey'


@app.route('/')
def index(): 
    if "counter" not in session: 
        session["counter"] = 0
    session["counter"]+=1
    return render_template("index.html", counter=session["counter"])

app.run(debug=True)
