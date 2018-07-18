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
    print("list of users (1): " + str(users))
    if username:
        login_status = "Yes"
        return render_template("index.html", username=username, login_status=login_status, votes=votes)
    else:
        username = "blank"
        login_status = "No"
        login_error = "No"
        return render_template("index.html", username=username, login_status=login_status, login_error=login_error, votes=votes)


#Get input value from login.html and check if given username/password exist in db.
@app.route("/loginPost", methods=['POST'])
def loginPost():
    username = request.form.get("username")
    if username in users:
        username = "blank"
        login_status = "No"
        login_error = "Yes"
        print("list of users (2): " + str(users))
        print("login status: " + login_status)
        print("login error: " + login_error)
        return redirect(url_for('index', username=username, login_status=login_status, login_error=login_error, votes=votes))
    else:
        users.append(username)
        session['user'] = username
        login_status = "Yes"
        login_error = "No"
        print("list of users (2): " + str(users))
        print("login status: " + login_status)
        print("login error: " + login_error)
        return redirect(url_for('index', username=username, login_status=login_status, login_error=login_error, votes=votes))


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
