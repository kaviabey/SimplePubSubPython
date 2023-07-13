import socket
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
       

       client_socket.connect((HOST,PORT))
       while True:
 
        
 
        # ask the client whether he wants to continue
        message = input()
          # message sent to server
        client_socket.send(message.encode('ascii'))
        data = client_socket.recv(1024)
        if message != 'terminated':
            continue
        else:
            break
    
       client_socket.close()
      #  msg = input()
      #  client_socket.sendall(msg.encode('utf-8'))
       

       
