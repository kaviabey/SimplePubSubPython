import socket
import sys
import threading

HOST = sys.argv[1]
PORT = int(sys.argv[2])
TYPE = sys.argv[3]
def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print('\n' + data.decode('ascii'))

def send_messages(client_socket):
    while True:
        message = input("Enter your message: ")
        client_socket.send(message.encode('ascii'))
        if message.upper() == 'TERMINATED':
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    args = tuple(sys.argv[3:])
    client_socket.sendall(' '.join(args).encode('ascii'))



    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()




#  msg = input()
#  client_socket.sendall(msg.encode('utf-8'))



