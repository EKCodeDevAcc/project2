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

    print("/ channelname: " + str(channelname))

    keyVal = [channelname]
    choosenChats = [d for d in chats if d['channel'] in keyVal]
    numChoosen = len(choosenChats)

    if numChoosen > 0:
        print("choosenChats: " + str(choosenChats[0]["time"]))
        print("numChoosen: " + str(numChoosen))

    # if numChoosen > 5:
    #     for idx, val in enumerate(choosenChats):
    # print(idx, val)


    if numChoosen > 5:
        for i in range(numChoosen-5):
            # choosenChats.remove(choosenChats[i]["time"])
            choosenChats = [d for d in choosenChats if d['time'] != choosenChats[0]["time"]]
            # chats = [d for d in chats if d['time'] != choosenChats[i]["time"]]
            print("for loop choosen: " + str(choosenChats))


    if username:
        login_status = "Yes"
        return render_template("index.html", username=username, login_status=login_status, channels=channels, choosenChats=choosenChats, channelname=channelname)
    else:
        username = "blank"
        login_status = "No"
        return render_template("index.html", username=username, login_status=login_status, channels=channels, choosenChats=choosenChats, channelname=channelname)


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
    print("post channelname: " + str(channelname))
    print("post channel session: " + str(session['channel']))
    login_status = "Yes"
    login_error = "No"
    username = session.get('user')
    #print("list of users (2): " + str(users))
    #print("login status: " + login_status)
    return redirect(url_for('index', username=username, login_status=login_status, channels=channels, channelname=channelname))



@socketio.on("update channel")
def channel(data):
    channelname = data["channelname"]
    print("socket: " + str(channelname))
    channels.append(channelname)
    print("socket channel list: " + str(channels))
    emit("channel updated", channels, broadcast=True)


#working on this part
# @socketio.on("switch channel")
# def switchChannel(data):
#     session.pop('channel', None)
#     channelname = data["channelname"]
#     print("get switch channel name: " + str(channelname))

#     session['channel'] = channelname

#     print("session: " + str(session['channel']))
#     emit("channel switched", channelname, broadcast=True)


@socketio.on("delete channel")
def deleteChannel(data):
    channelname = data["channelname"]
    print("delete channel socket: " + str(channelname))
    channels.remove(channelname)
    print("delete channel list socket: " + channels)
    #this part not using
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