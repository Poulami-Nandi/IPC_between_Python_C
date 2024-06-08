import threading
import socket
import queue
import random
import time
from enum import Enum

# Define an enum for message types
class MessageType(Enum):
    TYPE_A = 1
    TYPE_B = 2
    TYPE_C = 3
    TYPE_D = 4
    TYPE_E = 5

# Define a function for thread 1 (server)
def server_thread():
    # Create a tcp socket for communication
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    num_of_conn = 1000;
    server_socket.listen(num_of_conn)

    print("[ServerThread]: Server listening on {}:{}".format(*server_address))

    for i in range(num_of_conn):
        client_socket, client_address = server_socket.accept()
        print("[ServerThread]: Received ", i, "-th connection from", client_address)

        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            print("[ServerThread]: data is NULL")
            continue

        # Extract message type and payload
        message_type = MessageType(data[0])
        payload = data[1:]
        print("[ServerThread]: incoming message_type is: ", message_type)

        # Respond back to the client with the same message
        client_socket.sendall(data)

        # If the received message is of type TYPE_B, forward it to thread 2 via queue
        if message_type == MessageType.TYPE_B:
            my_queue.put(payload)


    print("[ServerThread]: closing server socket on {}:{}".format(*server_address))
    server_socket.close()

# Define a function for thread 2 (communication via queue)
def queue_thread():

    print("[QueueThread]: Queue thread started")

    while not force_exit:
        try:
            # Retrieve data from the queue
            data = my_queue.get(timeout=5)
        except queue.Empty:
            continue
        if not data:
            continue
        else:
            print("[QueueThread]: Received from queue:", data)
        if force_exit == True:
            print("[QueueThread]: Terminating Queue thread")
            break

# Define a function for thread 3 (client)
def client_thread():

    while True:
        # Create a socket for communication
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 12345)
        try:
            client_socket.connect(server_address)
        except ConnectionRefusedError:
            print("[ClientThread]: Server connection has been closed")
            break
        # Send a message to the server
        time.sleep(1)
        message_type = MessageType(random.randint(1,5))
        print("[ClientThread]: outgoing message_type: ", message_type)
        payload = b"0123456789"  # 10-byte payload
        full_message = message_type.value.to_bytes(1, 'big') + payload
        client_socket.sendall(full_message)

        # Receive response from the server
        response = client_socket.recv(1024)
        print("[ClientThread]: Received from server:", response.decode())
        print("[ClientThread]: Going to close socket with client")
        client_socket.close()

# create the queue
my_queue = queue.Queue()
force_exit = False
# Create and start the threads
thread1 = threading.Thread(target=server_thread)
thread2 = threading.Thread(target=queue_thread)
thread3 = threading.Thread(target=client_thread)

thread1.start()
thread2.start()
time.sleep(2)
thread3.start()

# Join server and clent threads
thread1.join()
print("[MainThread] Thread1 joined")
thread3.join()
print("[MainThread] Thread3 joined")
# set force_exit bool to true to intimate Thread2 to get terminated
force_exit = True
thread2.join()
print("[MainThread] All thread joined. Terminating main thread")
