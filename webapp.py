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
    return render_template('page1.html')

@app.route('/showFact')
def render_fact():
    quakes = []
    quakes = get_quake_options()
    return render_template('page1.html', location_options = quakes)    
    
def get_quake_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('earthquakes.json') as earthquakes_data:
        data = json.load(earthquakes_data)
    quakes_loc = []
    for a in quakes_loc:
        quakes_loc.append(a["location"]["full"])
    options=""
    for s in quakes_loc:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
if __name__=="__main__":
    app.run(debug=True)
    
    