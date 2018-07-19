import os
import requests

from flask import Flask, session, jsonify, render_template, request, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
from chat import newChat

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# list of all channels
channels = []

chats = []

# list of usernames
users = []

votes = ["what"]

@app.route("/")
def index():
    username = session.get('user')
    print("list of users (1): " + str(users))
    asd = newChat('testing', 'admin', 'Hi!', 'Today')
    print(asd)
    print(asd.channel)
    print(asd.time)
    chats.append(asd)
    print(chats)
    print(chats[0])
    print(chats[0].user)
    #print([d['channel'] for d in chats])
    if username:
        login_status = "Yes"
        return render_template("index.html", username=username, login_status=login_status, channels=channels)
    else:
        username = "blank"
        login_status = "No"
        return render_template("index.html", username=username, login_status=login_status, channels=channels)


#Get input value from login.html and check if given username/password exist in db.
@app.route("/loginPost", methods=['POST'])
def loginPost():
    username = request.form.get("username")
    users.append(username)
    session['user'] = username
    login_status = "Yes"
    login_error = "No"
    print("list of users (2): " + str(users))
    print("login status: " + login_status)
    return redirect(url_for('index', username=username, login_status=login_status, channels=channels))


#Logout user and redirect to '/' which in this case, login page.
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect('/')


@socketio.on("update channel")
def channel(data):
    channelname = data["channelname"]
    print(channelname)
    channels.append(channelname)
    print(channels)
    emit("channel updated", channels, broadcast=True)


@socketio.on("delete channel")
def deleteChannel(data):
    channelname = data["channelname"]
    print(channelname)
    channels.remove(channelname)
    print(channels)
    emit("channel deleted", channels, broadcast=True)