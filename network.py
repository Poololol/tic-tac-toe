import socket
import copy

defaultIP = '127.0.0.1'

class Packet:
    def __init__(self) -> None:
        pass

class Network:
    def __init__(self, ip: str | None = None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5)
        if ip and ip != '':
            self.server = ip
        else:
            self.server = defaultIP
        self.port = 5555
        self.addr = (self.server, self.port)
        self.playerOffset = 0
    def getPos(self):
        return self.pos
    def connect(self) -> str:
        try:
            print('Connecting...')
            self.client.connect(self.addr)
            message = self.client.recv(2048).decode()
            self.addr = self.client.getsockname()
            print(f'Connected to: {self.addr[0]}:{self.addr[1]}')
            return message
        except Exception as e:
            print('An Error Occurred whilst trying to Connect to the server:')
            return e
    def send(self, data, debug=False) -> str:
        try:
            #print('Sending...')
            self.client.send(str.encode(str(data)))
            if debug:
                print(f'Sent: {data}')
            reply = self.client.recv(2048).decode()
            if debug:
                print(f'Recieved: {reply}')
            return reply
        except socket.error as e:
            print(e)

    def sendAndRecieveData(self, data, dataLength: int = -1, debug: bool = False) -> dict:
        '''
        Sends the data to the server and returns the data recieved from the server as a dict
        
        :param data: Can be of any type but recommended to use a list of floats
        :param dataLength: Length of the data recieved which will usually be len(data), but could be different depending on use.
        If dataLength is not passed it will be set to len(data)
        :param debug: If True will print that data deing sent and recieved
        :returns: A dict with the structure of {'playerNum': Number of the current client, 'numPlayers': Total number of clients connected to the server, '#': most recent data recieved from client #}
        :rtype: dict
        '''
        if dataLength == -1:
            dataLength = len(data)
        recieved = copy.copy(str(self.send(data, debug=debug)))
        decoded = (int(recieved[1]), recieved[7:-1])
        decoded = (decoded[0], decoded[1].replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', '').split(','))
        for i,x in enumerate(decoded[1]):
            x = float(x)
            decoded[1][i] = x
        player = decoded[0]
        if int(recieved[4]) > 0:
            numPlayers = int(recieved[4])+self.playerOffset
        else:
            self.playerOffset = 1
            numPlayers = 1
        playerData = {'playerNum':player, 'NumPlayers':numPlayers}
        for playerNum in range(numPlayers):
            playerData[playerNum] = decoded[1][int(playerNum*dataLength):int(((playerNum+1)*dataLength))]
        return playerData