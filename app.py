from flask import Flask, redirect
app = Flask(__name__)

import task

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/scrobble")
def manual_scrobbling():
    task.start_scrobbling()

if __name__ == "__main__":
    app.run()
