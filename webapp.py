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

@app.route('/showFact')
def render_fact():
    quakes = get_quake_options()
    quakeFacts = get_quake_list()
    state = request.args["state"]
    inputVar = []
    for a in quakeFacts:
        if a["location"]["full"] == state:
            inputVar.append(a)
    info = "This is magnitude " + inputVar["impact"]["magnitude"] + " earthquake and a significance of " + inputVar["impact"]["significance"] + ". It has a gap of" + inputVar["impact"]["gap"] + ". It had a depth of " + inputVar["location"]["magnitude"] + " and was located at a latitude of" + inputVar["location"]["latitude"] + " and a longitude of " + inputVar["location"]["longitude"] + ". It happened on " + inputVar["time"]["month"] + "/" + inputVar["time"]["day"] + "/" + inputVar["time"]["year"] + " at " + inputVar["time"]["hour"] + ":" + inputVar["time"]["minute"] + "O'clock."
    return render_template('page1.html', location_options = quakes, info = info) 

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
    
if __name__=="__main__":
    app.run(debug=True)
    
    