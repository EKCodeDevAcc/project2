import os
import requests

from flask import Flask, session, jsonify, render_template, request, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# list of all channels
channel_list = ['general']

# list of usernames
users = []

votes = ["what"]

@app.route("/")
def index():
    username = session.get('user')
    print(users)
    if username:
        login_status = "Yes"
        print(login_status)
        return render_template("index.html", username=username, login_status=login_status, votes=votes)
    else:
        username = "blank"
        login_status = "No"
        print(login_status)
        return render_template("index.html", username=username, login_status=login_status, votes=votes)

#Get input value from login.html and check if given username/password exist in db.
@app.route("/loginPost", methods=['POST'])
def loginPost():
    username = request.form.get("username")
    users.append(username)
    print(users)
    session['user'] = username
    return redirect(url_for('index', username=username))

#Logout user and redirect to '/' which in this case, login page.
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect('/')

@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    print(selection)
    votes.append(selection)
    print(votes)
    emit("vote totals", votes, broadcast=True)
