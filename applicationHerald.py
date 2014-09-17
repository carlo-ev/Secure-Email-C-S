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
		user = self.get_user_from_message(jsonMesssage)
		action = jsonMessage["action"]
		if( user is not None ):
			if(islogged(user)):
				if action == "getMail":
					resp = self.getMail(user[0])
				elif action == "getContacts":
					resp = self.getContacts(user[0])
				elif action == "sendMail":
				elif action == "logout":
				else:
					print "Action not known"
					resp = '{ success: false, errors: "Action not known" }'
			else:
				print "Invalid Credencials Sent"
				resp = '{ success: false, errors: "Invalid Credentials"}'
		else:
			if action == "login":
				print "login"
				if self.login( str(jsonMessage["login"]["email"]), str(jsonMessage["login"]["password"]) ):
					key = "RandomKey"
					self.onlineUsers.append( (str(jsonMessage["login"]["email"]) , key) )
					resp = self.login_response( (str(jsonMessage["login"]["email"]), key, "" )
				else:
					resp = self.login_response( "", "", "Invalid Credentials" )
			elif action == "signup":
				print "signup"
				resp = "signup" 
			else:
				print "Action not known"
				resp = '{ success: False, errors: "Action not known" }'
		return resp

	def getContacts(self, user_email):
		print "Gettin user contacts"
		current_user self.session.query(User).filter( User.email==user_email ).all()
		contacts = current_user.contacts
		print contacts
		response = '{ successs: True, contacts: ['
		for cont in contacts:
			response += cont.toJSON()
			response += ', '
		response += '{} ] }'
		return response
																		 ' 
																		 
	def getMail(self, user_email):
		print "Gettin Mail for ", user_email
		messages = self.session.query(Message).filter( Message.receiver.like(user_email) ).all()
		print messages
		response = '{ succcess: True, messages: ['
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
					user = (json_user["email"], json_user["key"])
			return user
	
	def islogged(self, user):
		search = [ i for i, v in enumerate(self.onlineUsers) if i == user[0] and v == user[1] ]
		return len(search) > 0
	
	def login(self, email, password):
			print email
			print password
			user_to_login = self.session.query(User).filter(User.email==email).all()
			print user_to_login
			if len(user_to_login) > 0:
				print "User Found!"
				if users[0].password == password:
					return True
			return False

	def login_response(self, user, key, errors):
		response = '{'
		if errors == "":
				response += 'user: { '
				response += 'email: "' + user + '",'
				response += 'key: "' + key + '" '
				response += '}, '
				response += 'success: true'
		else:
			response += 'errors: "' + errors + '", '
			response += 'success: false'
		response += '}'
		return response