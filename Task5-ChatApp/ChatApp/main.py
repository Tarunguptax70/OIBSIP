from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)

rooms = {}
users = {}
PROFILE_PICS = [
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#ff7f50"/></svg>',
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#6495ed"/></svg>',
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#9acd32"/></svg>',
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#ee82ee"/></svg>',
    '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="50" fill="#ffdab9"/></svg>',
]

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break

    return code

def delayed_delete(room_code):
    socketio.sleep(5)
    if room_code in rooms and rooms[room_code]["members"] <= 0:
        print(f"Deleting empty room {room_code} after delay.")
        del rooms[room_code]

@app.route("/", methods=["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if not name or not password:
            return render_template("login.html", error="Please enter a name and password.", name=name)

        if name not in users or users[name]["password"] != password:
            return render_template("login.html", error="Invalid credentials.", name=name)

        session["name"] = name
        return redirect(url_for("lounge"))

    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if not name or not password:
            return render_template("signup.html", error="Please enter a name and password.", name=name)

        if name in users:
            return render_template("signup.html", error="Name already taken.", name=name)

        users[name] = {"password": password, "profile_pic": random.choice(PROFILE_PICS)}
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/lounge", methods=["POST", "GET"])
def lounge():
    name = session.get("name")
    if not name:
        return redirect(url_for("login"))

    if request.method == "POST":
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if join != False and not code:
            return render_template("lounge.html", error="Please enter a room code.", user=users.get(name))

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": [], "names": set()}
        elif code not in rooms:
            return render_template("lounge.html", error="Room does not exist.", user=users.get(name))

        session["room"] = room
        return redirect(url_for("room"))

    return render_template("lounge.html", user=users.get(name))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/account", methods=["GET", "POST"])
def account():
    if "name" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = session["name"]
        pic_index = int(request.form.get("profile_pic"))
        if 0 <= pic_index < len(PROFILE_PICS):
            users[name]["profile_pic"] = PROFILE_PICS[pic_index]
        return redirect(url_for("account"))

    return render_template("account.html", users=users, profile_pics=PROFILE_PICS)

@app.route("/room")
def room():
    if "name" not in session or "room" not in session or session["room"] not in rooms:
        return redirect(url_for("lounge"))

    room_code = session.get("room")
    return render_template("room.html", code=room_code, messages=rooms[room_code]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    name = session.get("name")
    if room not in rooms or name not in users:
        return

    now = datetime.now()
    current_time = now.strftime("%H:%M")
    content = {
        "name": name,
        "message": data["data"],
        "time": current_time,
        "profile_pic": users[name]["profile_pic"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name or name not in users:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    if name in rooms[room]["names"]:
        return False

    join_room(room)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    send({"name": name, "message": "has entered the room", "time": current_time, "profile_pic": users[name]["profile_pic"]}, to=room)
    rooms[room]["members"] += 1
    rooms[room]["names"].add(name)
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")

    if not room or not name or name not in users:
        return

    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        rooms[room]["names"].discard(name)
        if rooms[room]["members"] <= 0:
            socketio.start_background_task(delayed_delete, room)
    
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    send({"name": name, "message": "has left the room", "time": current_time, "profile_pic": users[name]["profile_pic"]}, to=room)
    print(f"{name} has left the room {room}")


@socketio.on("leave")
def leave(data):
    room = session.get("room")
    name = session.get("name")

    if not room or not name or name not in users:
        session.clear()
        return

    leave_room(room)
    profile_pic = users[name]["profile_pic"] # Get pic before clearing session

    if room in rooms:
        rooms[room]["members"] -= 1
        rooms[room]["names"].discard(name)
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    send({"name": name, "message": "has left the room", "time": current_time, "profile_pic": profile_pic}, to=room)
    print(f"{name} has left the room {room}")
    session.clear()

if __name__ == "__main__":
    socketio.run(app, debug=True)
