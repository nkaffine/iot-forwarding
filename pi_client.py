import receiver

class PiClient:
    def __init__(self):
        f = open("config.txt", "r")
        self.server_ip = f.readline()
        self.server_port = f.readline()
        self.receiver = receiver.Receiver(self.server_ip, int(self.server_port))

    def start(self):
        while True:
            self.receiver.initiateConnection()
            try:
                self.receiver.process()
            except ConnectionResetError:
                print("connection lost")

if __name__ == "__main__":
    client = PiClient()
    client.start()
