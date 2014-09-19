import smtplib

class ExternalDispatcher:

	credentials = dict()
	credentials["google"] = ('carlo_ev@unitec.edu', 'Semperfidelis9')
	credentials["hotmail"] = ('charliees92@hotmail.com', 'outofmysun12792')
	emailServers = dict()
	emailServers["google"] = 'smtp.gmail.com:587'
	emailServers["hotmail"] = 'smtp.live.com:587'

	def __init__(self, to, title, message):
		self.message = 'Subject: %s\n\n%s' % (title, message)
		if("google.com" in to):
			self.type = "google"
		else:
			self.type = "hotmail"
		self.destiny = to

	def send(self):
		server = smtplib.SMTP(emailServer[self.type])
		server.starttls()
		server.login(credentials[self.type][0], credentials[self.type][1])
		server.sendmail( credentials["google"][0], self.to, self.message )
		server.quit()
		print "Email sent from %s to %s" % (self.type, self.to)
