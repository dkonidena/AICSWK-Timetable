#Simple class representing a module, includes the name and a list of topics
#topics is a list of strings
#name is a string
class Module:
	def __init__(self,name="", topics=list()):
		self.name = name
		self.topics = topics

	#this is used during set up and should not be used in your solution
	def setName(self,name):
		self.name = name

	#this is used during set up and should not be used in your solution
	def setTopics(self,topics):
		self.topics = topics

	#this is used during set up and should not be used in your solution
	def addTopic(self,topic):
		self.topics.append(topic)

	def __str__(self):
		return str([self.name, self.topics])

	def __repr__(self):
		return str(self)