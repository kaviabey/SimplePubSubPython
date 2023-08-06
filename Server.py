import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = int(sys.argv[1])

subscribers = {}
publishers = {}
message_lock = threading.Lock()


def handle_client(conn):
    received_bytes = b""
    data = conn.recv(1024)
    received_bytes += data
    client_tuple = received_bytes.decode('ascii')
    client_type, identifier = client_tuple.split(' ')

    if client_type.upper() == 'PUBLISHER':
        print(f'PUBLISHER CONNECTED WITH THE TOPIC {identifier.upper()}')
        publishers[conn] = identifier.upper()
    elif client_type.upper() == 'SUBSCRIBER':
        print(f'SUBSCRIBER CONNECTED WHO IS INTERESTED IN {identifier.upper()}')
        subscribers[conn] = identifier.upper()

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print('\n Message from a client:  ' +data.decode('ascii'))

        if data.decode('ascii').upper() == 'TERMINATED':
            break

        if conn in publishers.keys():
            with message_lock:
                for subscriber in subscribers.keys():
                    if subscribers[subscriber] == publishers[conn]:
                        subscriber.sendall(data)
    conn.close()


def broadcast_thread():
    while True:
        msg = input("Enter message to broadcast:  ")
        broadcast(msg)


def broadcast(message):
    receivers = list(subscribers.keys()) + list(publishers.keys())
    with message_lock:
        for receiver in receivers:
            receiver.sendall(message.encode('ascii'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server is running .....")
    message_thread = threading.Thread(target=broadcast_thread)
    message_thread.start()
    while True:
        conn, addr = server_socket.accept()
        print('\n connected by', addr)

        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()
