import json, string, random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbBase import Base, User, Message, Contact
from datetime import datetime
from externalDispatcher import ExternalDispatcher
import Tkinter as tk

class ApplicationHerald:
	
	def puts(self, newText):
		self.gui.config(state='normal')
		self.gui.insert(tk.END, str(newText) + '\n')
		self.gui.config(state='disabled')

	def __init__(self, gui):
		self.engine = create_engine('sqlite:///secureEmail.sqlite3')
		Base.metadata.bind = self.engine
		DBSession = sessionmaker(bind=self.engine)
		self.session = DBSession()
		self.onlineUsers = []
		self.gui = gui

	def newRequest(self, message):
		jsonMessage = json.loads(message)
		self.puts(jsonMessage)
		user = self.get_user_from_message(jsonMessage)
		action = jsonMessage["action"]
		if( user is not None ):
			if(self.islogged(user)):
				if action == "getMail":
					self.puts("Action: GetMail")
					resp = self.getMail(user[0])
				elif action == "getContacts":
					self.puts("Action: GetContacts")
					resp = self.getContacts(user[0])
				elif action == "sendMail":
					self.puts("Action: SendMail")
					resp = self.sendMail(user, jsonMessage["mail"], user)
				elif action == "addContact":
					self.puts("Action: AddContact")
					resp = self.addContact(user, jsonMessage["contact"])
					
				elif action == "logout":
					self.puts("Action: Logout")
					self.remove_user_if_online(user)
					resp = '{ "success": "True", "errors": "None" }'
				else:
					self.puts("Action not known")
					resp = '{ "success": "False", "errors": "Action not known" }'
			else:
				self.puts("Invalid Credencials Sent")
				resp = '{ "success": "False", "errors": "Invalid Credentials"}'
		else:
			if action == "login":
				self.puts("Action: Login")
				prc_email = str(jsonMessage["login"]["email"])
				self.remove_user_if_online(prc_email)
				if self.login( prc_email, str(jsonMessage["login"]["password"]) ):
					sessionKey = self.create_session_key(prc_email)
					self.onlineUsers.append( (prc_email , sessionKey) )
					resp = self.login_response( prc_email, sessionKey, "" )
				else:
					resp = self.login_response( "", "", "Invalid Credentials" )
			elif action == "signup":
				self.puts("Action: Signup")
				credentials = jsonMessage["credentials"]
				resp = self.signup(credentials)
			else:
				self.puts("Action not known")
				resp = '{ "success": "False", "errors": "Action not known" }'
		return resp

	def sendMail(self, sender, message, user):
		titl = str(message["title"])
		bod = str(meessage["body"])
		date_time = str(datetime.now())
		list_of_receiver = str(message["receivers"]).split(";")
		for dest in list_of_receiver:
			if "@sercure.hn" not in dest:
				ext = ExternalDispatcher(dest, titl, bod)
		message_to_store = Message(title=titl,body=bod,sender=user[0],receiver=str(message["receivers"]),active=True,created_at=date_time)
		actual_user = self.sesssion.query(User).filter( User.email==user[0] ).all()[0]
		actual_user.messages.append(message_to_store)
		self.session.commit()
		return '{ "success": "True", "errors": "None" }'
				

	def addContact(self, user, contact_info):
		date_time = str(datetime.now())	
		new_username = str(contact_info["username"])
		actualUser = self.session.query(User).filter( User.email==user[0] ).all()[0]
		collliding_contact = [ v for v in actualUser.contacts if v.username==new_username ]
		if colliding_contact > 0:
			return '{ "success": "False", "errors": "User is already a contact!" }'
		else:
			contact = Contact(username=new_username, added_at=date_time, active=True)
			actualUser.contacts.append(contact)
			self.session.commit()
			return '{ "success": "True", "errors": "None"  }'

	def signup(self, credentials):
		new_email = str(credentials["email"])
		new_password = str(credentials["password"])
		colliding_users = self.session.query(User).filter( User.email==new_email ).all()
		if len(colliding_users) > 0:
			return '{ "success": "False", "errors": "Missing Credentials/User Already Exists"  }'
		else:
			date_time = str(datetime.now())
			new_user = User(email=new_email, password=new_password, active=True, created_at=date_time)
			self.session.add(new_user)
			self.session.commit()
			return '{ "success": "True", "errors": "None" }'

	def remove_user_if_online(self, email):
		for i, v in enumerate(self.onlineUsers):
			if v[0] == email:
				self.onlineUsers.remove(v)

	def getContacts(self, user_email):
		current_user = self.session.query(User).filter( User.email==user_email ).all()[0]
		contacts = current_user.contacts
		self.puts(contacts)
		response = '{ "successs": "True", "contacts": ['
		for cont in contacts:
			response += cont.toJSON()
			response += ', '
		response += '{} ] }'
		return response
										 
	def getMail(self, user_email):
		self.puts("Gettin Mail for "+user_email)
		messages = self.session.query(Message).filter( Message.receiver.like(user_email) ).all()
		self.puts(messages)
		response = '{ "succcess": True, "messages": ['
		for mess in messages:
			response += mess.toJSON()
			response += ', '
		response += '{} ] }'
		return response

	def get_user_from_message(self, json_message):
			user = None
			if "user" not in json_message:
				user = None
			else:
				json_user = json_message["user"]
				if "email" and "key" not in json_user:
					user = None
				else:
					user = (str(json_user["email"]), str(json_user["key"]))
			return user
	
	def islogged(self, user):
		search = [ v[0] for i, v in enumerate(self.onlineUsers) if v[0] == user[0] and v[1] == user[1] ]
		return len(search) > 0
	
	def login(self, email, password):
			self.puts(email)
			self.puts(password)
			user_to_login = self.session.query(User).filter(User.email==email).all()
			self.puts(user_to_login)
			if len(user_to_login) > 0:
				self.puts("User Found!")
				if user_to_login[0].password == password:
					self.puts("Login Successful")
					return True
			self.puts("Login Failed!")
			return False

	def create_session_key(self, email):
			return ''.join( random.choice( string.ascii_uppercase + email + string.digits + string.ascii_lowercase ) for _ in range(64) )
		
	def login_response(self, user, key, errors):
		if errors == "":
			response = '{ "user": { "email": "%s", "key": "%s" }, "success": "True" }' % ( user, key)
		else:
			response = '{ "errors": "%s", "success": "False" }' % (errors)
		return response
