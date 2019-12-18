import module
import tutor

#This class is used to create the time table object that you will assign a schedule to
#Importantly, it creates a dictionary, of dictionaries. Each day of the week is it's own dictionary, which can have a key value pair assigned to it.
#The key will be the slot number, and the value a list of objects that is the tutor, module and sessiontype in that order.
#Tutor will be a tutor object, module will be a module object and sessionType is a string that should be either 'module' or 'lab'
class Timetable:

	def __init__(self, taskNumber):
		self.schedule = {"Monday" : {}, "Tuesday" : {}, "Wednesday" : {}, "Thursday" : {}, "Friday" : {}}
		self.cost = 0
		self.taskNumber = taskNumber


	#This method is used to retrieve the [tutor, module, sessionType] tuple for a given timeslot on a given day.
	def getSession(self, day, timeslot):
		if day not in self.schedule:
			raise ValueError("Day can only be Monday, Tuesday, Wednesday, Thursday or Friday")
		else:
			if timeslot in self.schedule[day]:
				return self.schedule[day][timeslot]
			else:
				raise ValueError("timeslot not yet assigned")

	#This method is a simple boolean test to see if the given timeslot on the given day has been assigned.
	#It will return true if it has been assigned, and false if it has not.
	def sessionAssigned(self,day,timeslot):
		if day not in self.schedule:
			raise ValueError("Day can only be Monday, Tuesday, Wednesday, Thursday or Friday")
		else:
			if timeslot in self.schedule[day]:
				return True
			else:
				return False

	#This method will take all the information needed to assign a tutor and a module to a particular slot.
	#day should be one of the days of the working week, as defined in the schedule dictionary above
	#timeslot should be a number between and including 1-5 or 1-10 based on the task being attempted.
	#Tutor should be a tutor object
	#Module should be a module object
	#sessionType should be either 'module' or 'lab'
	def addSession(self, day, timeslot, tutor, module, sessionType):
		if day not in self.schedule:
			raise ValueError("Day can only be Monday, Tuesday, Wednesday, Thursday or Friday")
		elif self.taskNumber == 1:
			if timeslot == 0 or timeslot > 5:
				raise ValueError("timeslot can only be: 1, 2, 3, 4 or 5")
			else:
				self.schedule[day][timeslot] = [tutor, module, "module"]
		else:
			if timeslot == 0 or timeslot > 10:
				raise ValueError("timeslot can only be: 1, 2, 3, 4, 5, 6, 7, 8, 9 or 10")
			elif sessionType != "module" and sessionType != "lab":
				raise ValueError("sessionType must be either: module or lab") 
			else:
				self.schedule[day][timeslot] = [tutor, module, sessionType]

	#This method calls the correct checker based on the task
	def scheduleChecker(self, tutorList, moduleList):

		if self.taskNumber == 1:
			return self.task1Checker(tutorList, moduleList)
		else:
			return self.task23Checker(tutorList, moduleList)

	#Small utility method to check if a tutor can legally teach a module
	def canTeach(self, tutor, mod, isLab):
		#if its not a lab, we make sure every one of modules topics matches an expertise of the tutor
		if not isLab:
			topics = mod.topics

			i = 0
			for top in topics:
				if top not in tutor.expertise:
					print(str(mod.name) + " module session error.")
					return False

			return True

		#if it is a lab, we make sure the tutor and lab have at least one topic in common.
		else:
			topics = mod.topics

			i = 0
			for top in topics:
				if top in tutor.expertise:

					return True

			print(str(mod.name) + " lab session error.")
			return False	

	#A checker to make sure your task 1 schedule is legal. 
	def task1Checker(self, tutorList, moduleList):
		tutorCount = dict()
		modulesAssigned = list()
		scheduleCost = 0
		tutorsYesterday = list()
		#We make sure to check that every day has all its timeslots assigned
		for day in self.schedule:
			dayList = self.schedule[day]
			if len(dayList) != 5:
				print(str(day) + " does not have every slot assigned.")
				return False
			tutorsToday = list()

			#We then check the validty of each entry
			for entry in self.schedule[day]:
				[tut, mod, sessionType] = dayList[entry]

				#Make sure that each module is only taught once
				if mod.name in modulesAssigned:
					print(str(mod.name) + " is being taught twice.")
					return False
				else:
					modulesAssigned.append(mod.name)

				#We make sure every tutor is only teaching a single module a day
				if tut.name in tutorsToday:
					print(str(tut.name) + " is teaching multiple modules on " + str(day))
					return False
				else:
					tutorsToday.append(tut.name)

				#This makes sure a tutor is only teaching a maximun of two modules in a week
				if tut.name in tutorCount:
					modCount = tutorCount[tut.name]
					tutorCount[tut.name] = tutorCount[tut.name] + 1
					if modCount == 2:
						print(str(tut.name) + " is teaching more than 2 modules a week.")
						return False
				else:
					tutorCount[tut.name] = 1

				#Finally, we make sure that the tutor assinged to each module, is capable of teaching it. 
				if not self.canTeach(tut, mod, False):
					print(str(tut.name) + " can not teach module " + str(mod.name) + ", their expertise does not match the modules topic.")
					return False

			tutorsYesterday = tutorsToday

		return True


	#This checks the validity of a solution to problem 2 and 3, and also calculates the cost. 
	def task23Checker(self, tutorList, moduleList):

		tutorCount = dict()
		modulesAssigned = list()
		labsAssigned = list()
		scheduleCost = 0
		tutorsYesterday = list()
		modCount = dict()
		labCount = dict()
		taughtModuleYesterday = list()

		for tutor in tutorList:
			modCount[tutor.name] = 0
			labCount[tutor.name] = 0
			tutorCount[tutor.name] = 0


		for day in self.schedule:
			dayList = self.schedule[day]

			#Again, we check each day has all of its slots assigned
			if len(dayList) != 10:
				print(str(day) + " does not have every slot assigned.")
				return False

			tutorsToday = dict()
			possibleDiscount = dict()
			taughtModuleToday = list()

			#process the validity of each entry
			for entry in self.schedule[day]:
				[tut, mod, sessionType] = dayList[entry]

				#We check that each module has only a single entry for both module sessions and lab sessions
				if sessionType == "module":
					if mod.name in modulesAssigned:
						print(str(mod.name) + " is being taught twice.")
						return False
					else:
						modulesAssigned.append(mod.name)

				elif sessionType == "lab":
					if mod.name in labsAssigned:
						print(str(mod.name) + " has two lab sessions.")
						return False
					else:
						labsAssigned.append(mod.name)	

				#We make sure that an illegal session type hasn't been entered somehow
				else:
					print(str(mod.name) + " has been given a session that is not a module or a lab")
					return False

				#We now go through every tutor, and make sure they are not exceeding their credit limit.	
				if tut.name in tutorsToday:
					#This branch means the tutor is already teaching something today
					if tutorsToday[tut.name] >= 2:
						print(str(tut.name) + " is teaching two credits already on " + str(day))
						return False
					else:
						#We calculate the correct cost for the module
						if sessionType == "module":
							tutorsToday[tut.name] = tutorsToday[tut.name] + 2
							taughtModuleToday.append(tut)
							modCount[tut.name] = modCount[tut.name] + 1
							if modCount[tut.name] == 1:
								scheduleCost = scheduleCost + 500
							elif tut in taughtModuleYesterday:
								scheduleCost = scheduleCost + 100
							else:
								scheduleCost = scheduleCost + 300
						else:
							#We calculate the cost of a lab session
							tutorsToday[tut.name] = tutorsToday[tut.name] + 1
							labCount[tut.name] = labCount[tut.name] + 1
							initialLabCost = (300 - (50 * labCount[tut.name])) / 2
							scheduleCost = scheduleCost + initialLabCost

							if tut.name in possibleDiscount:
								scheduleCost = scheduleCost - possibleDiscount.pop(tut.name)
				else:
					#This branch means the tutor has not yet taught something else today
					#We calculate the costs correspondingly
					if sessionType == "module":
						tutorsToday[tut.name] = 2
						taughtModuleToday.append(tut)
						modCount[tut.name] = modCount[tut.name] + 1
						if modCount[tut.name] == 1:
							scheduleCost = scheduleCost + 500
						elif tut in taughtModuleYesterday:
							scheduleCost = scheduleCost + 100
						else:
							scheduleCost = scheduleCost + 300
					else:
						tutorsToday[tut.name] = 1

						labCount[tut.name] = labCount[tut.name] + 1
						initialLabCost = (300 - (50 * labCount[tut.name]))
						scheduleCost = scheduleCost + initialLabCost
						possibleDiscount[tut.name] = initialLabCost / 2

				#We update the credits the tutor is teaching overall
				if sessionType == "module":
					tutorCount[tut.name] = tutorCount[tut.name] + 2
				else:
					tutorCount[tut.name] = tutorCount[tut.name] + 1

				#Make sure tutor does not exceed their credit limit
				if tutorCount[tut.name] > 4:
						print(str(tut.name) + " is teaching already teaching the max amount of credits")
						return False

				#check is the tutor can legally teach the session, we use a boolean expression to determine if we're evaluating a module or lab session
				if not self.canTeach(tut, mod, sessionType=="lab"):
					print(str(tut.name) + " can not teach module " + str(mod.name) + ", their expertise does not match the modules topic.")
					return False				

			#One last check to make sure daily credits haven't been exceeded
			for name in tutorsToday:
				if tutorsToday[name] > 2:
					print(str(name) + " is teaching more than 2 credits today")
					return False

			tutorsYesterday = tutorsToday
			taughtModuleYesterday = taughtModuleToday

		#One final check to make sure total credits haven't been exceeded
		for name in tutorCount:
			if tutorCount[name] > 4:
				print(str(name) + " is teaching more than 4 credits overall")
				return False

		#If we get here, schedule is legal, so we assign the cost and return True
		self.cost = scheduleCost
		return True	

























