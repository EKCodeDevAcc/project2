import os
import requests

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# list of all channels
channel_list = ['general']

votes = []

@app.route("/")
def index():
    return render_template("index.html", votes=votes)


@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    print(selection)
    votes.append(selection + '1234')
    print(votes)
    emit("vote totals", votes, broadcast=True)
