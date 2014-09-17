import socket
import json

client = socket.socket()
host = "127.0.0.1"
port = 9999

client.connect((host, port))
print client.recv(1024)
messageToSend =  '{ "action": "login", "login":{"email":"user@user", "password":"password1"}}'
client.send(messageToSend)
print client.recv(1024)
client.send("end")
client.close()
