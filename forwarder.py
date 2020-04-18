import socket
import threading
import packet as p
import json


# This class takes in data and forwards to a device connected via tcp.
class Forwarder:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 10000
        # launching a thread to look for a connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.conn = None
        t1 = threading.Thread(target=self.__lookForConnections)
        t1.start()

    # Accepts the given data and returns whether or not the data was accepted.
    def acceptData(self, data):
        # Right not does not cover case where the socket fails
        if self.conn is None:
            if not self.isSearching:
                t1 = threading.Thread(target=self.__lookForConnections)
                t1.start()
            return False
        else:
            packets = p.Packet.encodeData(data)
            for packet in packets:
                self.conn.send(packet.encode().encode())
            return True

    # Searches for a connection.
    def __lookForConnections(self):
        self.isSearching = True
        self.socket.listen()
        # I assume that accept is blocking
        conn, addr = self.socket.accept()
        print('Connected by', addr)
        self.conn = conn
        self.isSearching = False


if __name__ == "__main__":
    forwarder = Forwarder()
    while True:
        data = input("Data to send: ")
        result = forwarder.acceptData(data)
        print(result)
