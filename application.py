import os
import requests
import datetime
import json

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
choosenChats = []

# list of usernames
users = []

votes = ["what"]

@app.route("/")
def index():
    username = session.get('user')
    channelname = session.get('channel')

    print(len(chats))

    if username:
        login_status = "Yes"
        return render_template("index.html", username=username, login_status=login_status, channels=channels, chats=chats, channelname=channelname)
    else:
        username = "blank"
        login_status = "No"
        return render_template("index.html", username=username, login_status=login_status, channels=channels, chats=chats, channelname=channelname)


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


#Get input value from login.html and check if given username/password exist in db.
@app.route("/channelSelectPost", methods=['POST'])
def channelSelectPost():
    session.pop('channel', None)
    channelname = request.form.get("hiddenChannel")
    #users.append(username)
    session['channel'] = channelname
    print("channelname: " + str(channelname))
    print(session['channel'])
    login_status = "Yes"
    login_error = "No"
    username = session.get('user')
    #print("list of users (2): " + str(users))
    #print("login status: " + login_status)
    return redirect(url_for('index', username=username, login_status=login_status, channels=channels, channelname=channelname))



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


@socketio.on("update chat")
def chat(data):

    channelname = session.get('channel')
    print(channelname)

    username = session.get('user')
    print(username)

    chatname = data["chat"]
    print(chatname)

    chattime = datetime.datetime.now()
    print(chattime)

    jsChat = "{\"channel\": \"" + channelname + "\", \"user\": \"" + username + "\", \"message\": \"" + chatname + "\", \"time\": \"" + str(chattime) + "\"}"
    #print(addChat)

    dictChat = dict(channel=channelname, user=username, message=chatname, time=str(chattime))

    chats.append(dictChat);

    foodict = {k: v for k, v in dictChat.items() if k.startswith('foo')}

    #print(chats[0].channel)

    emit("chat updated", jsChat, broadcast=True)

    # addChat = newChat('Testing', username, chatname, chattime)

    # chats.append(addChat)
    # print(chats)
    # print(chats[0].channel)
    # print(chats[0].user)
    # print(chats[0].message)
    # print(chats[0].time)

    #testJson = json.dumps(addChat)
    # testJson = json.dumps(addChat, indent=4, sort_keys=True, default=str)
    # print("1: " + testJson)
    # print("2: " + testJson[0])

    #emit("chat updated", testJson, broadcast=True)