from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import Namespace, emit
from random import randint

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdf1234"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


def emit_random_numbers():
    while True:
        yield randint(0, 100)


def bg_job():
    for i, n in enumerate(emit_random_numbers()):
        print(n)
        socketio.emit("data", n)
        socketio.sleep(0.0001)
        if i > 50000:
            break


@socketio.on("clicked")
def handle_data():
    print("sending data")
    thread = socketio.start_background_task(bg_job)


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
@socketio.on("connect")
def handle_connect():
    print("connected")
    print()


#
#
# @socketio.on("my event")
# def handle_my_custom_event(json):
#     print("received json: " + str(json))
#     print()


socketio.run(app, use_reloader=True, port=5001)
