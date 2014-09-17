import socket
from applicationHerald import ApplicationHerald

class Server:

	def __init__(self, host, port, queue=999):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((host, port))
		self.socket.listen(queue)
		self.herald = ApplicationHerald();		

	
	def run(self):
		print "Server Running"
		while True:
			clientSocket, clientAddress = self.socket.accept()
			print ('Cliente ', clientAddress,' Connected')
			clientSocket.send("Email Server Online")
			currentMessage = ""
			currentMessage = clientSocket.recv(1024)
			while(currentMessage != "end"):
				response = self.herald.newRequest(currentMessage)
				clientSocket.send(response)
				currentMessage = clientSocket.recv(1024)
			clientSocket.send("end")
			clientSocket.close()
