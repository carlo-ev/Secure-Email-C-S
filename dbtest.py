from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbBase import Base, User, Message, Contact
from datetime import datetime

print "Creating connection to DB"
engine = create_engine('sqlite:///secureEmail.sqlite3')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

print "Query a User"
print session.query(User).all()
print session.query(Message).all()
print session.query(Contact).all()
#user = session.query(User).filter(User.email=='user@user').all()
#print session.query(Contact).all()
#print user[0].contacts
#fecha = str(datetime.now())

#contact = Contact(username="user@user",added_at=fecha,active=True)

#user[0].contacts.append(contact)

#print user[0].contacts

#newUser = User(email="user2@user", password="password2", active=True, created_at=fecha)

#session.add(newUser)
#session.commit()
print "User Saved!"
