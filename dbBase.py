from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime


Base = declarative_base()

class User(Base):
	__tablename__ = 'users'
	
	id = Column( Integer, primary_key=True )
	email = Column( String(32) )
	password = Column( String(100) )
	active = Column( Boolean )
	created_at = Column( String(26) )
	messages = relationship("Message")
	contacts = relationship("Contact")

	def __repr__(self):
		return "<User (id='%s', email='%s', password='%s', active='%s', messages='%s', contacts='%s', created_at='%s')>" % (self.id, self.email, self.password, self.active, self.messages, self.contacts, self.created_at)

	def toJSON(self):
		return '{ "id": "%s", "email": "%s", "password": "%s", "active": "%s", "created_at": "%s" }' % (self.id, self.email, self.password, self.active, self.created_at)

class Message(Base):
	__tablename__ = 'messages'

	id = Column( Integer, primary_key=True )
	title = Column( String(32) )
	body = Column( Text )
	sender = Column( Integer, ForeignKey(User.id) )
	receiver = Column( String(32) )  
	active = Column( Boolean )
	created_at = Column( String(26) )

	def __repr__(self):
		return "<Message (id='%s', title='%s', body='%s', sender='%s', receiver='%s', active='%s', created_at='%s')>" % (self.id, self.title, self.body, self.sender, self.receiver, self.active, self.created_at)
	
	def toJSON(self):
		return '{ "id": "%s", "title": "%s", "body": "%s", "sender": "%s", "receiver": "%s", "active": "%s", "created_at": "%s"}' % (self.id, self.title, self.body, self.sender, self.receiver, self.active, self.created_at)

class Contact(Base):
	__tablename__ = 'contacts'

	id = Column( Integer, primary_key=True )
	user_id = Column( Integer, ForeignKey(User.id) )
	username = Column( String(32) )
	added_at = Column( String(26) )
	active = Column( Boolean )

	def __repr__(self):
		return "<Contact (id='%s', user_id='%s', username='%s', active='%s', added_at='%s')>" % (self.id, self.user_id, self.username, self.active, self.added_at)

	def toJSON(self):
		return '{ "id": "%s", "user_id": "%s", "username": "%s", "active": "%s", "added_at": "%s"}' % (self.id, self.user_id, self.username, self.active, self.added_at)

engine = create_engine('sqlite:///secureEmail.sqlite3')

Base.metadata.create_all(engine)

