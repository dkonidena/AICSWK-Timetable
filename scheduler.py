import module
import tutor
import ReaderWriter
import timetable
import random
import math

class Scheduler:

	def __init__(self,tutorList, moduleList):
		self.tutorList = tutorList
		self.moduleList = moduleList

	#Using the tutorlist and modulelist, create a timetable of 5 slots for each of the 5 work days of the week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, Smith, CS101, "module")
	#This line will set the session slot '1' on Monday to the module CS101, taught by tutor Smith. 
	#Note here that Smith is a tutor object and CS101 is a module object, they are not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in tasks 2 and 3. 
	#Tutor (3rd argument) and module (4th argument) can be assigned any value, but if the tutor or module is not in the original lists, 
	#	your solution will be marked incorrectly. 
	#The final, 5th argument, is the session type. For task 1, all sessions should be "module". For task 2 and 3, you should assign either "module" or "lab" as the session type.
	#Every module needs one "module" and one "lab" session type. 
	
	#moduleList is a list of Module objects. A Module object, 'm' has the following attributes:
	# m.name  - the name of the module
	# m.topics - a list of strings, describing the topics that module covers e.g. ["Robotics", "Databases"]

	#tutorList is a list of Tutor objects. A Tutor object, 't', has the following attributes:
	# t.name - the name of the tutor
	# t.expertise - a list of strings, describing the expertise of the tutor. 

	#For Task 1:
	#Keep in mind that a tutor can only teach a module if the module's topics are a subset of the tutor's expertise. 
	#Furthermore, a tutor can only teach one module a day, and a maximum of two modules over the course of the week.
	#There will always be 25 modules, one for each slot in the week, but the number of tutors will vary.
	#In some problems, modules will cover 2 topics and in others, 3.
	#A tutor will have between 3-8 different expertise fields. 

	#For Task 2 and 3:
	#A tutor can only teach a lab if they have at least one expertise that matches the topics of the lab
	#Tutors can only manage a 'credit' load of 4, where modules are worth 2 and labs are worth 1.
	#A tutor can not teach more than 2 credits per day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need. 
	#Furthermore, you should not import anything else beyond what has been imported above. 

	#This method should return a timetable object with a schedule that is legal according to all constraints of task 1.
	def domains(self, slots, modules, tutors):
		return {"modules":modules, 
		"tutors":tutors, 
		"days":["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], 
		"slots":slots}
	# choosing the module with minimum tutors available (tutors are dynamically updated in all the places)
	def moduleChoose(self, moduleDomain, tutorDomain, slotDomain):
		minTutors = math.inf
		minModule = {}
		# choosing the module with the least tutors available
		for module in moduleDomain:
			if len(moduleDomain[module]) < minTutors:
				minModule.clear()
				minModule[module] = moduleDomain[module]
				minTutors = len(moduleDomain[module])
			elif len(moduleDomain[module]) == minTutors:
				minModule[module] = moduleDomain[module]
		# from the modules chosen along with the tutors, choosing the tutor with the max available days
		# which implies the max available slots - checking slots too
		selected = {}
		maxDays = -1
		for module in minModule:
			for tutor in minModule[module]:
				if len(tutorDomain[tutor][0]) > maxDays and tutorDomain[tutor][1] > 0:
					selected.clear()
					selected[module] = []
					selected[module].append(tutor)
					maxDays = len(tutorDomain[tutor][0])
				elif len(tutorDomain[tutor][0]) == maxDays and tutorDomain[tutor][1] > 0:
					if module in selected:
						selected[module].append(tutor)
					else:
						selected[module] = []
						selected[module].append(tutor)
		if maxDays > 0:
			print("possible")
		else:
			print("no possible soln") # if in the checking nothing changed
		slotsAssigned = self.slotCheck(slotDomain, tutorDomain, selected)
		assginment = self.maxSlots(slotsAssigned, slotDomain)
		
		return assginment

	def maxSlots(self, slotsAssigned, slotDomain):
		maxSlots = 0
		day = None
		module = None
		tutor = None
		for slots in slotsAssigned:
			# from the assigned slots for all the modules, finalise the one with the day having the most slots
			if slotDomain[slotsAssigned[slots][1]] > maxSlots:
				maxSlots = slotDomain[slotsAssigned[slots][1]]
				day = slotsAssigned[slots][1]
				module = slots
				tutor = slotsAssigned[slots][0]
		return (module,tutor,day)

	# if slot domain value is 0 then day should also be deleted
	def slotCheck(self, slotDomain, tutorDomain, selected):
		available = {}
		found = False
		for module in selected:
			available[module] = {}
			for tutor in selected[module]:
				for day in slotDomain:
					if day in tutorDomain[tutor][0]:
						available[module] = [tutor, day]
						found = True
						break
				if found:
					break
		# a dict of modules: and tutors with days
		return available


	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)
		domain = self.domains([1,2,3,4,5], self.moduleList, self.tutorList)
		slotDomain = {}
		for day in domain["days"]:
			slotDomain[day] = 5
		moduleDomain = {}
		for module in domain["modules"]:
			moduleDomain[module] = self.eligibleTutors(module, True)
		tutorDomain = {}
		for tutor in domain["tutors"]:
			tutorDomain[tutor] = [domain["days"].copy(), 2]
		while(moduleDomain):
			x = self.moduleChoose(moduleDomain, tutorDomain, slotDomain)
			if(x[0] != None or x[1] != None or x[2] != None):
				timetableObj.addSession(x[2], slotDomain[x[2]], x[1], x[0], "module")
				del moduleDomain[x[0]]
				slotDomain[x[2]] -=1
				if(slotDomain[x[2]] == 0):
					del slotDomain[x[2]]
				tutorDomain[x[1]][0].remove(x[2])
				tutorDomain[x[1]][1] -=1
				print(x)
				print(tutorDomain[x[1]])
			else:
				print("backtrack")
				# need to implement backtrack	
		print(slotDomain)
		
		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		# self.randomModSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	#Now, we have introduced lab sessions. Each day now has ten sessions, and there is a lab session as well as a module session.
	#All module and lab sessions must be assigned to a slot, and each module and lab session require a tutor.
	#The tutor does not need to be the same for the module and lab session.
	#A tutor can teach a lab session if their expertise includes at least one topic covered by the module.
	#We are now concerned with 'credits'. A tutor can teach a maximum of 4 credits. Lab sessions are 1 credit, module sessiosn are 2 credits.
	#A tutor cannot teach more than 2 credits a day.
	def createLabSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)
		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.		
		self.randomModAndLabSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	#It costs £500 to hire a tutor for a single module.
	#If we hire a tutor to teach a 2nd module, it only costs £300. (meaning 2 modules cost £800 compared to £1000)
	#If those two modules are taught on consecutive days, the second module only costs £100. (meaning 2 modules cost £600 compared to £1000)

	#It costs £250 to hire a tutor for a lab session, and then £50 less for each extra lab session (£200, £150 and £100)
	#If a lab occurs on the same day as anything else a tutor teaches, then its cost is halved. 

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible. 
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here. 
	def createMinCostSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(3)

		#Here is where you schedule your timetable

		#This line generates a random timetable, that may not be valid. You can use this or delete it.
		self.randomModAndLabSchedule(timetableObj)

		#Do not change this line
		return timetableObj


	#This simplistic approach merely assigns each module to a random tutor, iterating through the timetable. 
	def randomModSchedule(self, timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "module")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	#This simplistic approach merely assigns each module and lab to a random tutor, iterating through the timetable.
	def randomModAndLabSchedule(self, timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "module")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

		for module in self.moduleList:
			tut = self.tutorList[random.randrange(0, len(self.tutorList))]

			timetableObj.addSession(days[dayNumber], sessionNumber, tut, module, "lab")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1
	# true for module and false for lab
	def tutorCanTeach(self, tutor, module, labOrModule):
		if labOrModule:
			return (all(x in tutor.expertise for x in module.topics))
		else:
			return (any(x in tutor.expertise for x in module.topics))

	def eligibleModules(self, tutor, labOrModule):
		modules = []
		for x in self.moduleList:
			if(self.tutorCanTeach(tutor, x, labOrModule)):
				modules.append(x)
		return modules
	
	def eligibleTutors(self, module, labOrModule):
		tutors = []
		for x in self.tutorList:
			if(self.tutorCanTeach(x, module, labOrModule)):
				tutors.append(x)
		return tutors		

























