import socket
import time
import packet as p


# This class takes in data and forwards to a device connected via tcp.
class Receiver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # launching a thread to look for a connection
    def initiateConnection(self):
        shouldContinue = True
        while shouldContinue:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            didSucceed = (self.socket.connect_ex((self.host, self.port)) == 0)
            shouldContinue = not didSucceed
            if not didSucceed:
                print("connection failed")
                time.sleep(2.5)

    # use to combine packets into data chunks
    def readData(self):
        print("is reading data")
        receivedData = ""
        shouldContinue = True
        while shouldContinue:
            data = self.socket.recv(p.Packet.packetSize)
            if len(data) == 0:
                raise ConnectionResetError("connection closed")
            decoded = data.decode()
            packet = p.Packet.decode(decoded)
            receivedData += packet.data
            shouldContinue = not packet.isEnd
        return receivedData

    def process(self):
        print("is processing")
        while True:
            data = self.readData()
            print(data)

if __name__ == "__main__":
    receiver = Receiver('127.0.0.1', 10000)
    while True:
        receiver.initiateConnection()
        try:
            receiver.process()
        except ConnectionResetError:
            print("connection closed")

