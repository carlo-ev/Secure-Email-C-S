import socket
import Tkinter as tk
from applicationHerald import ApplicationHerald

class Server:

	def puts(self, newText):
		self.gui.config(state='normal')
		self.gui.insert(tk.END,  str(newText) + '\n')
		self.gui.config(state='disabled')

	def __init__(self, host, port, gui, queue=999):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((host, port))
		self.socket.listen(queue)
		self.gui = gui
		self.herald = ApplicationHerald(gui);		

	
	def run(self):
		self.puts("Server Running")
		while True:
			clientSocket, clientAddress = self.socket.accept()
			self.puts("New Connection Inbound...\n")
			self.puts('Cliente '+str(clientAddress)+' Connected')
			clientSocket.send("Email Server Online")
			currentMessage = ""
			currentMessage = clientSocket.recv(1024)
			while(currentMessage != "end"):
				response = self.herald.newRequest(currentMessage)
				clientSocket.send(response)
				currentMessage = clientSocket.recv(1024)
			clientSocket.send("end")
			clientSocket.close()
