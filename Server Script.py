import socket
import threading

host = '127.0.0.1'
port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
nicknames_clients = []

def broadcast(message):
    for client in clients:
        client.send(message)

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}.")

        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames_clients.append(nickname)
        clients.append(client)

        print(f"Nickname of the client: {nickname}")
        broadcast(f"{nickname} client is connected to the server.\n".encode('utf-8'))
        client.send("Connected to the server.".encode('utf-8'))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames_clients[clients.index(client)]}:", message)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames_clients[index]
            nicknames_clients.remove(nickname)
            break

print("Server is running...")
receive()