#!/usr/bin/env python

"""harpy.py: Module Description ..."""

__author__ = "Minos Galanakis"
__license__ = "LGPL"
__version__ = "0.0.1"
__email__ = "minos197@gmail.com"
__project__ = "harpy"
__date__ = "25-09-2015"

from flask import Flask, render_template, request, url_for
from collections import OrderedDict
import datetime
import copy

#Test DataSet
dt = ('server1', 'router2', 'playstation3')

def tabularize_data(headers, data):
    """ Generate an html table from dictionary data """

    # Create the table header
    table_data = "<table border=\"1\" style=\"width:300px\"><thead><tr>"
    for h in headers:
      table_data += "<th>%s</th>"%h
    table_data += "</tr></thead>"

    #Create Table Body
    table_rows = ""
    for entry in data.keys():
      entry_dt = data[entry]
      table_rows += "<tr><td>%s</td>"%entry
      for e in entry_dt.keys():
        table_rows += "<td>%s</td>"% entry_dt[e]
      table_rows += "</tr>"
    
    table_data += table_rows
    table_data += "</table>"

    #print table_data
    return table_data

def gen_radio_buttons(gtype, label, data):
    """Generate a radio buttong group for dynamic forms"""

    form = "<label for=\"%s\">%s:</label>\n"%(gtype,label)
    headers = ["IP","MAC","Hostname","Alias","Select"]
    #make a copy of the dictionary
    temp_data = copy.deepcopy(data)
    
    for entry in temp_data.keys():
      temp_data[entry]['button']= "<input type=\"radio\" name=\"%s\" value=\"%s\" /><br />"%(gtype,temp_data[entry]["mac"])

    return tabularize_data(headers,temp_data)

app = Flask(__name__)

@app.route("/")
def main():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    headers = ["IP","MAC","Hostname","Alias"]
    templateData = {
        'title': 'Harpy!',
        'time': timeString,
        'dmap': tabularize_data(headers,data_d)
    }
    return render_template('index.html', **templateData)

@app.route('/add')
def add():
  # Create the buttons
  data = gen_radio_buttons("macdata", "Select the device  you wish to bind", data_d)
  return render_template('form_add.html', dyndata = data)

@app.route('/form/', methods=['POST'])
def form():
    alias     = request.form['alias']
    if not len(alias): alias = "N.A"
    color     = request.form['color']
    mac_adddr = request.form['macdata']
    return render_template(
        'form_action.html',
        alias=alias,
        color=color,
        maddr=mac_adddr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7777, debug=True)
