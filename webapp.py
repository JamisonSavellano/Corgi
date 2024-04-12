from flask import Flask, request, url_for, render_template, request
from markupsafe import Markup

import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')    
    
@app.route("/p1")
def render_page1():
    quakes = get_quake_options()
    return render_template('page1.html', location_options = quakes)
    
@app.route("/p2")
def render_page2():
    quakes = get_month_options()
    return render_template('page2.html', month_options = quakes)

@app.route('/showFact')
def render_fact():
    quakes = get_quake_options()
    quakeFacts = get_quake_list()
    state = request.args["state"]
    inputVar = []
    for a in quakeFacts:
        if a["location"]["full"] == state:
            inputVar.append(a)
    info = ""
    info = "This is magnitude " + str(inputVar[0]["impact"]["magnitude"]) + " earthquake and a significance of " + str(inputVar[0]["impact"]["significance"]) + ". It has a gap of " + str(inputVar[0]["impact"]["gap"]) + ". It had a depth of " + str(inputVar[0]["location"]["depth"]) + " and was located at a latitude of " + str(inputVar[0]["location"]["latitude"]) + " and a longitude of " + str(inputVar[0]["location"]["longitude"]) + ". It happened on " + str(inputVar[0]["time"]["month"]) + "/" + str(inputVar[0]["time"]["day"]) + "/" + str(inputVar[0]["time"]["year"]) + " at " + str(inputVar[0]["time"]["hour"]) + ":" + str(inputVar[0]["time"]["minute"]) + "O'clock."
    return render_template('page1.html', location_options = quakes, info = info) 
    
    
@app.route('/showFact2')
def render_fact2():
    quakes = get_month_options()
    quakeFacts = get_quake_list()
    state = request.args["state"]
    mags = get_mag(int(state))
    inputVar = []
    for a in quakeFacts:
        if int(a["time"]["month"]) == int(state):
            inputVar.append(a)
    options = Organize_dates(inputVar)
    newData = get_graph(options, mags)
    lenght = newData.length
    return render_template('Graph1.html', month_options = quakes, newData = newData, mags = mags, length = length)

def Organize_dates(data):
    Orangized = []
    preOrganized = []
    for d in data:
        preOrganized.append(d["time"]["year"])
        preOrganized.append(d["time"]["month"])
        preOrganized.append(d["time"]["day"])
        Orangized.append(preOrganized)
        preOrganized = []
    return Orangized
    
def get_mag(data):
    mag = []
    temp = get_quake_list()
    for d in temp:
        if d["time"]["month"] == data:
            mag.append(d["impact"]["magnitude"])
    return mag
    
def get_graph(option, mag):
    mags = mag
    options = option
    newData = []
    temp = 0.0
    z = 0
    for a in options:
        temp = mags[z]
        newData.append({"x": a, "y": temp})
        z += 1
    return newData

def get_quake_list():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('earthquakes.json') as earthquakes_data:
        data = json.load(earthquakes_data)
    return data    
    
def get_quake_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('earthquakes.json') as earthquakes_data:
        data = json.load(earthquakes_data)
    quakes_loc = []
    for a in data:
        quakes_loc.append(a["location"]["full"])
    options=""
    for s in quakes_loc:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
def get_month_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('earthquakes.json') as earthquakes_data:
        data = json.load(earthquakes_data)
    quakes_month = []
    m = []
    for a in data:
        quakes_month.append(a["time"]["month"])
        m.append(a["time"]["month"])
    options=""
    x = 0
    for s in quakes_month:
        x+=1
        if m[x] != s:
            m.append(s)
            options += Markup("<option value=\"" + str(s) + "\">" + str(s) + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
if __name__=="__main__":
    app.run(debug=True)
    
    