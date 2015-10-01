#!/usr/bin/env python

"""harpy.py: Module Description ..."""

__author__ = "Minos Galanakis"
__license__ = "LGPL"
__version__ = "0.0.1"
__email__ = "minos197@gmail.com"
__project__ = "harpy"
__date__ = "25-09-2015"

from flask import Flask, render_template, request, url_for, copy_current_request_context
from flask.ext.socketio import SocketIO, emit

from threading import Thread, Event

from time import sleep
import datetime


from formatutils import *
from updater import PageUpdater

#Test DataSet
# TODO remove it when testing is complete
from test_dataset import get_data
data_d = get_data()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['SERVER_NAME']='localhost:7777'

# Wrap the app to a socketit for async tasks
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()

@app.route("/")
def main():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'Harpy!',
        'time': timeString
    }
    return render_template('index.html', **templateData)

@app.route('/add')
def add():
  # Create the buttons
  
  data = gen_radio_buttons("ipsel", "Select the device  you wish to bind", thread.get_table())
  return render_template('form_add.html', dyndata = data)

@app.route('/form/', methods=['POST'])
def form():
    alias     = request.form['alias']
    if not len(alias): alias = "N.A"
    color     = request.form['color']
    ipsel = request.form['ipsel']
    
    arp_entry = thread.get_table()[ipsel]
    thread.clear_color(color)
    arp_entry['color'] = color
    if len(alias): arp_entry['alias'] = alias

    return render_template(
        'form_action.html',
        alias = alias,
        color = color,
        maddr = arp_entry["mac"])

@socketio.on('connect', namespace='/autoreload')
def auto_reload():

    global thread
    print('Client connected')

    # Only start if it its not already started
    if not thread.isAlive():
        print "Starting Thread"
        thread = PageUpdater(socketio)
        thread.start()

@socketio.on('disconnect', namespace='/autoreload')
def test_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    socketio.run(app)
