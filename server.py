from flask import Flask
from threading import Thread
from SheetsDatabase import number

app = Flask(__name__)

@app.route("/")
def home():
    return f"Hello! this is the main page {number}"

if __name__ == "__main__":
    app.run()

def run():
    app.run(host = '0.0.0.0', port = 8080)

def run_server():
    t = Thread(target = run)
    t.start()