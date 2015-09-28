#!/usr/bin/env python

"""harpy.py: Module Description ..."""

__author__ = "Minos Galanakis"
__license__ = "LGPL"
__version__ = "0.0.1"
__email__ = "minos197@gmail.com"
__project__ = "harpy"
__date__ = "25-09-2015"

from flask import Flask, render_template, request, url_for
import datetime

#Test DataSet
dt = ('server1', 'router2', 'playstation3')

app = Flask(__name__)

def gen_radio_buttons(gtype, label, data):
    """Generate a radio buttong group for dynamic forms"""
    form = "<label for=\"%s\">%s:</label>\n"%(gtype,label)
    for entry in data:
        form += "<input type=\"radio\" name=\"%s\" value=\"%s\" />%s<br />\n"\
            % ( gtype, entry.lower(), entry)
    return form


@app.route("/")
def main():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'HELLO!',
        'time': timeString
    }
    # Create the buttons
    data = gen_radio_buttons("macdata", "Select the device  you wish to bind", dt)
    return render_template('form_add.html', dyndata = data)


@app.route('/form/', methods=['POST'])
def form():
    alias     = request.form['alias']
    color     = request.form['color']
    mac_adddr = request.form['macdata']
    return render_template(
        'form_action.html',
        alias=alias,
        color=color,
        maddr=mac_adddr)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7777, debug=True)
