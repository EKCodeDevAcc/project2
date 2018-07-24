import os
import requests
import datetime
import json

from flask import Flask, session, jsonify, render_template, request, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# list of all channels.
channels = []

# list of all chats.
chats = []

# list of chats belong to certain channel.
choosenChats = []

# list of usernames.
users = []

# max number of chats.
maxChats = 100

#Get informations and pass variables when the page is loaded.
@app.route("/")
def index():
    #Get current username and current channelname.
    username = session.get('user')
    channelname = session.get('channel')

    global chats

    #Set current channelname as key value, and get list of dictionary where its channel name matches with key value.
    keyVal = [channelname]
    choosenChats = [d for d in chats if d['channel'] in keyVal]

    #Check how many chats with choosen channel name are there.
    numChoosen = len(choosenChats)

    #If there are more than allowed number of chats, which in this case 100, for the amount of difference, remove oldest chats from the list.
    if numChoosen > maxChats:
        for i in range(numChoosen-maxChats):
            choosenChats = [d for d in choosenChats if d['time'] != choosenChats[0]["time"]]
            chats = [d for d in chats if d['time'] != choosenChats[0]["time"]]

    #If a user is logged in, send all information with login status "Yes" which allows users to see other contents.
    #If login status is "No", a user only can see login box.
    if username:
        login_status = "Yes"
        return render_template("index.html", username=username, login_status=login_status, channels=channels, choosenChats=choosenChats, channelname=channelname)
    else:
        username = ""
        login_status = "No"
        return render_template("index.html", username=username, login_status=login_status, channels=channels, choosenChats=choosenChats, channelname=channelname)


#Get input value from login.html and check if given username/password exist
@app.route("/login", methods=['GET'])
def login():
    #Get input username and check if same username already exist or not.
    username = request.args.get("username")

    #If username already exist, shoot login error which alrets user an error message
    if username in users:
        username = ""
        login_status = "No"
        login_error = "Yes"
        data = dict(username=username, login_status=login_status, login_error=login_error)
        return jsonify(data)

    #If not, allow the user to login.
    else:
        users.append(username)
        session['user'] = username
        login_status = "Yes"
        login_error = "No"
        data = dict(username=username, login_status=login_status, login_error=login_error)
        return jsonify(data)


#Logout user.
@app.route("/logout", methods=['GET'])
def logout():
    username = request.args.get("username")

    # A line below is used to remove username from the list, but if application got closed while user still logged in, session caused an issue so I disabled it.
    # users.remove(username)

    session.pop('user', None)
    login_status = "No"
    login_error = "No"
    data = dict(username="", login_status=login_status, login_error=login_error)
    return jsonify(data)


#Get channel name and gets chats belong to the selected channel and send it back to the page.
@app.route("/channelSelect", methods=['GET'])
def channelSelectPost():

    #Remove previous channel name and add newly selected channel name.
    session.pop('channel', None)
    channelname = request.args.get("channelname")
    session['channel'] = channelname

    #Same as def login() part.
    global chats

    keyVal = [channelname]
    choosenChats = [d for d in chats if d['channel'] in keyVal]
    numChoosen = len(choosenChats)

    if numChoosen > maxChats:
        for i in range(numChoosen-maxChats):
            choosenChats = [d for d in choosenChats if d['time'] != choosenChats[0]["time"]]
            chats = [d for d in chats if d['time'] != choosenChats[0]["time"]]

    data = dict(channelname=channelname, channellength=numChoosen, chats=choosenChats)
    return jsonify(data)


#When users request new channel name, check its validity and send results back.
@socketio.on("update channel")
def channel(data):
    channelname = data["channelname"]

    #If same channelname already exist, send error message and emit to channel exist which pops out alert box to the user who requested the channel.
    if channelname in channels:
        error_message = "Channel already exist"
        username = session.get('user')

        #combine error_message and username and send it to channel exist.
        send_data = str(error_message) + "/" + str(username)
        emit("channel exist", send_data, broadcast=True)

    #Add the requested channel to channel list.
    else:
        channels.append(channelname)
        emit("channel updated", channels, broadcast=True)


#When user request to delete, remove channel from the list and send deleted channel name back to page.
@socketio.on("delete channel")
def deleteChannel(data):
    channelname = data["channelname"]
    channels.remove(channelname)
    emit("channel deleted", channelname, broadcast=True)


#Get information of new chat and send it back to the page.
@socketio.on("update chat")
def chat(data):

    #Get current channel, username, chat, and timestamp and add this as a new dictionary to chats list.
    channelname = data["channel"]
    username = session.get('user')
    chatname = data["chat"]
    chattime = datetime.datetime.now()

    jsChat = "{\"channel\": \"" + channelname + "\", \"user\": \"" + username + "\", \"message\": \"" + chatname + "\", \"time\": \"" + str(chattime) + "\"}"
    dictChat = dict(channel=channelname, user=username, message=chatname, time=str(chattime))
    chats.append(dictChat)
    emit("chat updated", jsChat, broadcast=True)