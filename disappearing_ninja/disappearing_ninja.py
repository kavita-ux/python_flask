'''
Kavita Amin
11/30/2017
Assignment: Disappearing Ninja
'''

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index(): 
    return render_template("index.html")

@app.route('/ninja')
def ninja(): 
    return render_template("ninja.html")
@app.route('/ninja/<ninja_color>')
def display_ninja(ninja_color): 
    return render_template("display_ninja.html", ninja_color = ninja_color)

app.run(debug=True)