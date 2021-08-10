#imports
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


# scope of the application
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(credentials)

# Open the spreadhseet
sheet = client.open("Zalando Data").worksheet("zalando_data")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()

def log_update():
    """
    Print number of rows every few seconds

    """
    #infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        values_list = sheet.col_values(1)
        # Insert the list as a row at index 8
        insertRow = ["GA111A28J-A11","Gabor","Trainers — weiß/ice","https://img01.ztat.net/article/spp-media-p1/bc1c433d1649346e9eb02d316961bfc9/dd8d3ad466d64631b956405046eb9ca1.jpg","£89.99","https://www.zalando.co.uk/gabor-trainers-weissice-ga111a28j-a11.html"]
        sheet.insert_row(insertRow, 8)
        number = len(values_list)
        print(number)
        socketio.emit('newnumber', {'number': number}, namespace='/test')
        socketio.sleep(5)


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the log thread only if the thread has not been started before.
    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(log_update)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)