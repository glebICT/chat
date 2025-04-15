import socket
import threading

# Client configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The server's port

# Get the client's nickname
nickname = input("Choose your nickname: ")

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client.connect((HOST, PORT))
except socket.error as e:
    print(f"Connection error: {e}")
    exit()

# Function to receive messages from the server
def receive():
    while True:
        try:
            # Receive message (decode from bytes to string)
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # If there's an error (e.g., server disconnects), close the client
            print("Error occurred!")
            client.close()
            break

# Function to send messages to the server
def write():
    while True:
        message = input('')
        client.send(message.encode('utf-8'))

# Create threads for receiving and sending messages
receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

# Start the threads
receive_thread.start()
write_thread.start()
