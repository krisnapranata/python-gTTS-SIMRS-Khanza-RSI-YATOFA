import socket

s = socket.socket()
s.connect(('127.0.0.1',12345))
text = "Open"
s.send(text.encode());
s.close()