from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbBase import Base, User, Message
from datetime import datetime

print "Creating connection to DB"
engine = create_engine('sqlite:///secureEmail.sqlite3')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

print "Query a User"
print session.query(User).all()
print session.query(User).filter(User.email=='user@user').all()
fecha = str(datetime.now())

#newUser = User(email="user2@user", password="password2", active=True, created_at=fecha)

#session.add(newUser)
#session.commit()
print "User Saved!"
