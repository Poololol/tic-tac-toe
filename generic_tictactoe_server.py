import socket
from threading import Thread
import network
import sys


def decodeReply(reply: str) -> list[float]:
    '''
    Decode the reply from a str to a list of floats
    '''
    decoded = reply.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', '').split(',')
    for i, x in enumerate(decoded):
        x = float(x)
        decoded[i] = x
    return decoded

def threaded_client(conn: socket.socket, player):
    global currentPlayer
    global prevCurrentPlayer
    data = 0
    conn.send(str.encode(str([0, 9, 9])))
    reply = ''
    while True:
        try:
            data = conn.recv(2048).decode()
            if debug:
                print(f"Received from #{player}: ", data)
            packet[player] = decodeReply(data)
            if data == None:
                print("Disconnected")
                break
            else:
                if currentPlayer - prevCurrentPlayer < 0:
                    reply = (player, 0, packet)
                else:
                    reply = (player, currentPlayer, packet)
                if debug:
                    print(f"Sending to #{player}: ", reply, end='\n')
            prevCurrentPlayer = currentPlayer
            conn.sendall(str.encode(str(reply)))
        except Exception as e:
            if debug:
                print(f"An Error has occured: {e}")
            break
    print(f"Lost connection: Client #{player} Closed\n")
    conn.close()
    currentPlayer -= 1
async def main2():
    currentPlayer = 0
    prevCurrentPlayer = 0
    packet = [[0] for _ in range(10)]
    
    print('To use a custom IP use --ip [ip]')
    args = sys.argv
    if '--ip' in args:
        server = args[args.index('--ip')+1] 
        print(f"Used User IP: {server}\n")
    elif '--debug' in args:
        debug = True
    else:
        debug = False
        server = network.defaultIP
        print(f"Used Default IP {server}\n")
    
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        print(str(e))
    s.listen()
    print("Waiting for a connection, Server Started\n")
    
    while True:
        conn, addr = s.accept()
        print("Connected to:", f'{addr[0]}:{addr[1]}', f'Player #{currentPlayer}')
        Thread(target=threaded_client, args=(conn, currentPlayer)).run()
        currentPlayer += 1
