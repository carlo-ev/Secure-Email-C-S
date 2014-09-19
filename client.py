import socket
import json
import Tkinter as tk
import thread
from PIL import Image, ImageTk

class Client:

	def __init__(self, server, port):
		self.server = server
		self.port = port
		self.session = None
		self.view_change_needed = True
		self.next_view = self.login

	def run(self):
		while True:
			if self.view_change_needed:
				if self.next_view is not None:
					thread.start_new_thread(self.next_view, ())
					self.view_change_needed = False
				else:
					break
	

	def login(self):
		self.login = tk.Tk()
		login_window = self.login
		login_window.grid()
		
		tk.Label(login_window, pady=15, padx=3, text="Secure Mail Login", justify=tk.CENTER).grid(column=1, row=0)
		
	# LEFT SIDE --> LOGIN
		tk.Label(login_window, pady=15, padx=3, text="Email:", justify=tk.CENTER).grid(column=0, row=1)
		self.email = tk.StringVar()
		tk.Entry(login_window, textvariable=self.email).grid(column=1, row=1)

		tk.Label(login_window, pady=15, padx=3, text="Password:", justify=tk.CENTER).grid(column=0, row=2)
		self.password = tk.StringVar()
		tk.Entry(login_window, textvariable=self.password, show='*').grid(column=1, row=2)

		tk.Button(login_window, text="Login", command=self.requestLogin).grid(column=2, row=3)

		self.errors = tk.StringVar()
		errors_label = tk.Label(login_window, pady=15, padx=3, textvariable=self.errors)
		errors_label.grid(column=1, row=4)

	# RIGHT SIDE --> SIGNUP
		tk.Label(login_window, pady=15, padx=3, text="Secure Mail SignUp", justify=tk.CENTER).grid(column=4, row=0)		

		tk.Label(login_window, pady=15, padx=3, text="Username:", justify=tk.CENTER).grid(column=3, row=1)
		self.signup_email = tk.StringVar()
		tk.Entry(login_window, textvariable=self.signup_email).grid(column=4, row=1)
		tk.Label(login_window, pady=15, padx=3, text="@secure.hn", justify=tk.LEFT).grid(column=5, row=1)

		tk.Label(login_window, pady=15, padx=3, text="Password:", justify=tk.CENTER).grid(column=3, row=2)
		self.signup_pass = tk.StringVar()
		tk.Entry(login_window, textvariable=self.signup_pass, show='*').grid(column=4, row=2)
		
		tk.Button(login_window, text="SignUp", command=self.requestSignup).grid(column=4, row=3)
		self.signup_errors = tk.StringVar() 
		tk.Label(login_window, textvariable=self.signup_errors).grid(column=4, row=4)

	# WINDOW
		login_window.title('Secure Email Login')
		login_window.geometry('650x220')
		login_window.mainloop()
		
		

	def requestLogin(self):
		self.errors.set("")
		data = ', "login": { "email": "%s", "password": "%s" }' % (self.email.get(), self.password.get())
		respJSON = self.simpleRequest('login', data)
		if(str(respJSON["success"]) == "True"):
			print("login successful")
			self.session = (respJSON["user"]["email"], respJSON["user"]["key"])
			self.login.destroy()
			self.next_view = self.home
			self.view_change_needed = True
		else:
			self.errors.set(str(respJSON["errors"]))
	
	def requestSignup(self):
		if(self.signup_pass.get() != "" and self.signup_email.get() != ""):
			self.signup_errors.set("")
			data = ', "credentials": { "email": "%s", "password": "%s" }' % (self.signup_email.get()+'@secure.hn', self.signup_pass.get())
			respJSON = self.simpleRequest('signup', data)
			if(str(respJSON["success"]) == "True"):
				self.signup_email.set("")
				self.signup_pass.set("")
				self.signup_errors.set("User created Successfully!\nGo Ahead and Login!")
			else:
				self.signup_errors.set(str(respJSON["errors"]))
		else:
			self.signup_errors.set("All entries are Required!")	

	def home(self):
		print("home!!!")
		home = tk.Tk()
		section1 = tk.Frame(home)	
		section1.grid(column=0, row=0)
		section2 = tk.Frame(home)
		section2.grid(column=0, row=1)
		section3 = tk.Frame(home)
		section3.grid(column=1, row=1)
		
		# MENU
		title_label = tk.Label(section1, text="Inbox, justify=tk.CENTER")

		contacts_button = tk.Button(section1, justify=tk.CENTER, text="View Contacts")
		contacts_button.grid(column=3, row=0)			

		new_button = tk.Button(section1, justify=tk.CENTER, text="New Email")
		new_button.grid(column=4, row=0)

		# INBOX
		inbox_label = tk.Label(section2, justify=tk.CENTER, text="Your Recent Emails")
		inbox_label.grid(column=0, row=0)
	
		email_list_box = tk.Listbox(section2)
		email_list_box.insert(1, "First Email")
		email_list_box.grid(column=0, row=1)
		scroll = tk.Scroll(section2, command=email_list_box.yview)
		email_list_box['yscrollcommand'] = scroll.set
		scroll.grid(column=1, row=1)


		# READ EMAIL
		tk.Label(section3, justify=tk.CENTER, text="Selected Email").grid(column=0, row=0)
		tk.Label(section3, justify=tk.CENTER, text="From:").grid(column=0, row=1)
		from_text = tk.Entry(section3, )

		home.title("Secure Email - Home!")
		home.geometry('800x350')
		home.mainloop()


	def simpleRequest(self, action, data):
		connection = socket.socket()
		connection.connect((self.server, self.port))
		connection.recv(1024)
		session_string = (', "user": { "email": "%s", "key": "%s" }' % (self.session[0], self.session[1])) if self.session is not None else ""
		message_to_send = '{ "action": "%s" %s %s  }' % (action, data, session_string)
		connection.send(message_to_send)
		resp = connection.recv(1024)
		connection.send("end")
		connection.close()
		respJSON = json.loads(resp)
		return respJSON


client = Client('127.0.0.1', 9999)
client.run()

'''
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

client.send(messageToSend)
#messageToSend = '{ "action": "getContacts" }'

print client.recv(1024)

client.send("end")
client.close()
'''
