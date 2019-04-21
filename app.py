from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import Namespace, emit
from random import randint

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdf1234"
socketio = SocketIO(app)
thread = None
thread_lock = Lock()


@app.route("/")
def index():
    return render_template("index.html", async_mode=socketio.async_mode)


def emit_random_numbers():
    while True:
        yield randint(0, 100)


def bg_job(x):
    global thread
    for i, n in enumerate(emit_random_numbers()):
        print(n)
        socketio.emit("data", n)
        socketio.sleep(0.001)
        if i > x:
            break
    thread = None


@socketio.on("connect")
def handle_connect():
    print("connected")
    print()


@socketio.on("clicked")
def handle_data(data):
    print("sending data")
    global thread
    with thread_lock:
        if thread is None:
            try:
                x = int(data["data"])
                thread = socketio.start_background_task(bg_job, x)
            except ValueError:
                pass


#
# class MyCustomNamespace(Namespace):
#     def on_connect(self):
#         print("connected")
#
#     def on_disconnect(self):
#         print("disconnected")
#
#     def on_message(self, data):
#         print("message", data)
#
#     def on_my_event(self, data):
#         print("my_event", data)
#
#
# socketio.on_namespace(MyCustomNamespace("/test"))
#

#


#
#
# @socketio.on("my event")
# def handle_my_custom_event(json):
#     print("received json: " + str(json))
#     print()


socketio.run(app, use_reloader=True, port=5001)
