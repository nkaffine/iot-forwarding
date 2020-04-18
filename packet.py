import json

class Packet:
    packetSize = 1024
    maxDataSize = packetSize - len(json.dumps({"end": True, "data": None}))

    def __init__(self, data, isEnd):
        if not isinstance(data, str):
            raise ValueError("data must be string")
        if len(data) > Packet.maxDataSize:
            raise ValueError("data is too long")
        self.data = data
        self.isEnd = isEnd

    def encode(self):
        result = {
            "end": self.isEnd,
            "data": self.data
        }
        return json.dumps(result)

    def __str__(self):
        return self.encode()

    @staticmethod
    def decode(packet):
        if isinstance(packet, str):
            decodedPacket = json.loads(packet)
            return Packet(decodedPacket["data"], decodedPacket["end"])
        else:
            raise ValueError("invalid packet")

    # Takes in data of arbitrary length and returns a list of packets that breaks down the data
    @staticmethod
    def encodeData(data):
        # Validate the data is a string
        if isinstance(data, str):
            maxDataSize = Packet.maxDataSize
            packets = []
            # this can be made more elegant
            numPackets = len(data) / maxDataSize
            numPackets = numPackets + 1 if len(data) % maxDataSize != 0 else numPackets
            for i in range(round(numPackets)):
                packets.append(Packet(data[i*maxDataSize:(i+1)*maxDataSize], i == (round(numPackets) - 1)))
            return packets
        else:
            raise ValueError("data must be string")

# if __name__ == "__main__":
#     # testing some encoding stuff
#     packets = Packet.encodeData("j"*1024)
#     for packet in packets:
#         print(packet)
