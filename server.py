import socket
from flask import Flask
from flask import request
import threading
import json

global socket_connection
global main_socket
app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    if socket_connection == False:
       return json.dumps({"success": False}, indent=4)
    else:
        if main_socket == False:
            return json.dumps({"success": False}, indent=4)
        else:
            main_socket.sendall(request.json)
            response = {"success":True}
            return json.dumps(response, indent=4)


def initialize_connection():
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 10000  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        global main_socket
        main_socket = s
        print("socket is listening")
        conn, addr = main_socket.accept()
        print('Connected by', addr)
        global socket_connection
        socket_connection = conn

def establish_connection():
    if main_socket == False:
        print("socket doesn't exist")
    else:
        try:
            conn, addr = main_socket.accept()
            with conn:
                print('Connected by', addr)
                global socket_connection
                socket_connection = conn
        except:
            print()
            return False

if __name__ == "__main__":
    global socket_connection
    socket_connection = False
    global main_socket
    main_socket = False
    t1 = threading.Thread(target=initialize_connection)
    t1.start()
    app.run()
