#!/usr/bin/env python3
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import os, time, sys
import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port
host = "127.0.0.1"
port = 12345

# Bind the socket to the address
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)

print("Listening for connections...")

while True:
    try:
        # Accept a connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        # Receive data from the client
        data = client_socket.recv(1024)
        data2 = data.decode()
        print(f"Received: {data.decode()}")
        if data2 == "Open" or data2 == "open":
            print("yes")
            os.system('python3.12 C:\\xampp\\htdocs\\panggil.py')
       
        # Send a response
        response = f"Received: {data.decode()}"
        client_socket.send(response.encode())
        
        # Close the connection
        client_socket.close()
        
    except KeyboardInterrupt:
        print('Program Selese')
        sys.exit(0)
