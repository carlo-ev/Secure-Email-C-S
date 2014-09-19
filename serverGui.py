from requestServer import Server
import Tkinter as tk
import thread

class ServerGui(tk.Frame):

	def __init__(self, master=None):
		tk.Tk.__init__(self,master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		self.startButton = tk.Button(self,text="Start Server", command=self.start)
		self.startButton.grid(row=0, column=1)

		self.serverLogText = tk.Text(self, padx="10", pady="5", bg='#000000', fg='#ffffff', width='89', height='20')
		self.serverLogText.grid(row=1, column=1)
		self.serverLogText.insert(tk.END, "----------------------------------Server Console Output----------------------------------\n")
		self.serverLogText.config(state='disabled')
		
		scroll = tk.Scrollbar(self, command=self.serverLogText.yview )
		self.serverLogText['yscrollcommand'] = scroll.set
		scroll.grid(row=1, column=2, sticky='nsew')
	

	def start(self):
		print "Start Server!"	
		server = Server('127.0.0.1',9999, self.serverLogText)
		thread.start_new_thread(server.run, ())
		self.startButton.config(state='disabled')

sGui = ServerGui()
sGui.master.title('Secure Server GUI')
sGui.master.geometry("660x300")
sGui.mainloop()
