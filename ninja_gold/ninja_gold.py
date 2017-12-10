"""
Kavita Amin 
12/1/2017

Assignment: Build a mini game that helps a ninja make some money! 
When you start the game, your ninja should have 0 gold. 
The ninja can go to different places (farm, cave, house, casino) and earn different amounts of gold. 
In the case of a casino, your ninja can earn or LOSE up to 50 golds. 

"""

from flask import Flask, render_template, session, redirect, request
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "key"

@app.route('/')
def index(): 

    if "gold" not in session: 
        session["gold"] = 0

    if "activities" not in session: 
        session["activities"] = []    

    return render_template("index.html")



@app.route('/process_money', methods=["POST"])
def process_money(): 
    
    time = str(datetime.now())

    if request.form["building"] == "farm": 
        farmEarnings = random.randint(10, 20)
        session["gold"] += farmEarnings
        session["activities"].append("Earned {} golds from the farm! ({}) ".format(farmEarnings,time))
    elif request.form["building"] == "cave":
        caveEarnings = random.randint(5, 10)
        session["gold"] += caveEarnings
        session["activities"].append("Earned {} golds from the cave! ({}) ".format(caveEarnings,time))
    elif request.form["building"] == "house": 
        houseEarnings = random.randint(2, 5)
        session["gold"] += houseEarnings
        session["activities"].append("Earned {} golds from the house! ({}) ".format(houseEarnings,time))
    elif request.form["building"] == "casino": 
        winOrLose = random.randint(0,1)
        if winOrLose == 0: 
            casinoLoss = random.randint(0,50)
            session["gold"]-= casinoLoss
            session["activities"].append("Entered a casino and lost {} golds. ({}) ".format(casinoLoss, time))
        elif winOrLose == 1: 
            casinoWin = random.randint(0, 50)
            session["gold"] += casinoWin
            session["activities"].append("Entered a casino and won {} golds. ({}) ".format(casinoWin, time))

    return redirect('/')

app.run(debug=True)
