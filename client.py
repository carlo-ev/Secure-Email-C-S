import socket
import json

client = socket.socket()
host = "127.0.0.1"
port = 9999

client.connect((host, port))
print client.recv(1024)

messageToSend =  '{ "action": "login", "login":{"email":"user@user", "password":"password1"}}'


client.send(messageToSend)

first = client.recv(1024)
print first

js = json.loads(first)

print js
print js["user"]
print js["user"]["email"]
print js["user"]["key"]

messageToSend = '{ "action": "getContacts", "user": { "email": "%s", "key": "%s" } }' % ( str(js["user"]["email"]), str(js["user"]["key"]) )

print messageToSend

#client.send(messageToSend)
#messageToSend = '{ "action": "getContacts" }'

#print client.recv(1024)

client.send("end")
client.close()
