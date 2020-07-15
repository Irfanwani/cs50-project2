import os
import requests

from flask import Flask, render_template, jsonify, request, flash, session, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

users_list = []

channels_list = []

channel_joined = {}

message_list = {}


@app.route("/")
def index():
    username = request.form.get("username")
    if "username" in session:
        flash(f"Already logged in as {session['username']}", "info")
        return redirect(url_for("channels"))
    if request.method == "POST":
        if username == user:
            flash("Username already taken!", "info")
            return render_template("index.html")
        if len(username) < 3 or username is None:
            flash("Username must contain 3 or more characters", "info")
            return render_template("index.html")
        return redirect(url_for("channels"))
    return render_template("index.html")


@app.route("/channels", methods=["GET", "POST"])
def channels():
    username = request.form.get("username")
    if "username" in session:
        return render_template("channels.html", username=session["username"], chnls=channels_list)
    if request.method == "POST":
        if username in users_list:
            flash("Username already taken!", "info")
            return render_template("index.html")
        if len(username) < 3 or username is None:
            flash("Username must contain 3 or more characters", "info")
            return render_template("index.html")
        session["username"] = username
        users_list.append(username)
        flash(f"{session['username']}, you logged in successfully!", "info")
        return render_template("channels.html", username=session["username"], chnls=channels_list)
    else:
        flash("Please login first.", "info")
        return redirect(url_for("index"))


@app.route("/channels/<int:channel_id>")
def channel(channel_id):
    chnl = channels_list[channel_id]
    if chnl is None:
        flash("No such channel", "info")
        return render_template("channels.html", username=session["username"], chnls=channels_list)
    return render_template("channel.html", users=channel_joined[chnl], chnl=chnl, chnls=channels_list)
    


@app.route("/chat", methods=["GET", "POST"])
def chat():
    channel = request.form.get("channel")
    if "channel" in session:
        flash(f"You are already joined in {session['channel']} channel.", "info")
        return render_template("chat.html", username=session["username"], msgs=message_list[session["channel"]])
    if request.method == "POST":
        if channel in channels_list:
            flash("channel name already taken.", "info")
            return render_template("channels.html", username=session['username'], chnls=channels_list)
        if len(channel) < 3 or channel is None:
            flash("Channel name should be 3 characters or more", "info")
            return render_template("channels.html", username=session["username"], chnls=channels_list)
        session["channel"] = channel
        channels_list.append(channel)
        message_list[session["channel"]] = []
        channel_joined[session["channel"]] = [session["username"]]
        flash(f"{session['channel']} created as a new channel!", "info")
        return render_template("chat.html", username=session["username"], msgs=message_list[session["channel"]])
    else:
        flash("Please join or create a channel to start chatting.", "info")
        return render_template("channels.html", username=session["username"], chnls=channels_list)


@app.route("/chat1/<int:channel_id>")
def chat1(channel_id):
    if "username" in session:
        chnl = channels_list[channel_id]

        # Allowing a user to join only a single channel
        if "channel" in session:
            return redirect(url_for("chat"))
        session["channel"] = chnl
        channel_joined[chnl].append(session["username"])
        flash(f"You joined the channel {session['channel']}", "info")
        return render_template("chat.html", username=session["username"], msgs=message_list[session["channel"]])
    else:
        flash("You are not logged in.Please login first.", "info")
        return redirect(url_for("index"))


@app.route('/logout')
def logout():
    usr = session['username']
    if "username" in session:
        if usr in users_list:
            users_list.remove(usr)
        session.pop("username", None)
        flash("Logged out successfully.", 'info')
        return redirect(url_for("index"))
    else:
        flash("You are not logged in.", "info")
        return redirect(url_for("index"))


@app.route('/leavechannel')
def leavechannel():
    if "username" in session:
        if "channel" in session:
            channel_joined[session["channel"]].remove(session["username"])
            session.pop("channel", None)
            flash("You left the channel", "info")
            return redirect(url_for("chat"))
        else:
            flash("You are not joined in any channel.", "info")
            return redirect(url_for('chat'))
    else:
        flash("you are not logged in.", "info")
        return redirect(url_for(index))


@socketio.on('send message')
def chatting(data):
    message = data['message']
    timestamp = data['timestamp']
    user = session["username"]
    message_list[session["channel"]].insert(0, f"{timestamp}- {user}:  {message} ")
    if len(message_list[session["channel"]]) > 100:
        message_list[session["channel"]].pop()
        
    emit('show message', {"message": message, 'user': user, 'timestamp': timestamp}, broadcast=True)
