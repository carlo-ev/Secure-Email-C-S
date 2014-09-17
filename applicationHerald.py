import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbBase import Base, User, Message, Contact
from datetime import datetime


class ApplicationHerald:
	
	def __init__(self):
		self.engine = create_engine('sqlite:///secureEmail.sqlite3')
		Base.metadata.bind = self.engine
		DBSession = sessionmaker(bind=self.engine)
		self.session = DBSession()
		self.onlineUsers = []

	def newRequest(self, message):
		jsonMessage = json.loads(message)
		print jsonMessage
		action = jsonMessage["action"]
		if "user" not in jsonMessage:
			user = ""
		else:
			user = jsonMessage["user"]
		response = ""
		if( action == "login" ):
			print "login"
			email = str(jsonMessage["login"]["email"])
			print email
			password = str(jsonMessage["login"]["password"])
			print password
			user_to_login = self.session.query(User).filter(User.email.like(email)).all()
			print user_to_login
			if len(users) > 0:
				print "User Found!"
				if users[0].password == password:
					key = "RandomKey"
					self.onlineUsers.append((users[0].email, key))
					print "Login Accepted!"
					response = "{ user: {"
					response +=  "email: " + users[0].email + ", key: " key
					response += 
					response = "{success: true}"
				else:
					print "Sorry Username/Password didnt match"
					response = "{success: false, errors: 'username/password incorrect'}"	
			else:
				print "User not found!"
				response = "{success: false, errors: 'username/password incorrect'}"	
		elif( action == "getMail" ):
			print "get mail"
			if user != "":
				
				messages = self.session.query(Message).filter() 
		elif( action == "getContacts" ):
			#make get contacts
			print "get Contacts"
		elif( action == "sendMail" ):
			#make send mail
			print "send an email"
		elif( action == "logout" ):
			#make logout
			print "logout user"
		else:
			#make 
			print "action not know"
		return response
