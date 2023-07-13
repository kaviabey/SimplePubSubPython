import socket
import threading 
import sys

HOST = '127.0.0.1'
PORT = int(sys.argv[1])



def handle_client(conn):
        while True:
         data = conn.recv(1024)
         print(data.decode('ascii'))
         if data.decode('ascii') == 'terminated':
             break
         data.sendall(data.encode('ascii'))
        conn.close()      

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
       server_socket.bind((HOST,PORT))
       server_socket.listen()
       
       while True:
        conn , addr = server_socket.accept()
        print('connected by', addr)
        client_thread = threading.Thread(target=handle_client, args=(conn))
        client_thread.start()
       