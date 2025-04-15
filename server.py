import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)

# List to store connected clients and their names
clients = []
nicknames = []

# Function to broadcast a message to all connected clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            # If a client disconnects abruptly, remove them
            index = clients.index(client)
            remove_client(index)

# Function to handle individual client connections
def handle_client(client):
    while True:
        try:
            # Receive message from the client (decode from bytes to string)
            message = client.recv(1024).decode('utf-8')
            # Broadcast the message to all other clients
            broadcast(f"{nicknames[clients.index(client)]}: {message}".encode('utf-8'))
        except:
            # If there's an error (e.g., client disconnects), remove the client
            index = clients.index(client)
            remove_client(index)
            break

# Function to remove a client
def remove_client(index):
    nickname = nicknames[index]
    client_to_remove = clients[index]
    clients.remove(client_to_remove)
    nicknames.remove(nickname)
    broadcast(f'{nickname} left the chat!'.encode('utf-8'))
    client_to_remove.close()

# Main function to start the server
def main():
    # Create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Bind the socket to the host and port
        server.bind((HOST, PORT))
    except socket.error as e:
        print(f"Socket binding error: {e}")
        return

    # Listen for incoming connections (allow up to 5 pending connections)
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        # Accept a new connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request and store the client's nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Broadcast that the client has joined
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))

        # Create a new thread to handle this client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()
