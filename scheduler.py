import module
import tutor
import ReaderWriter
import timetable
import random
import math
import time
'''
	This is the class which depicts the node in the search tree.
	It stores the assignment of a given slot i.e. - 
		1. Module
		2. Tutor
		3. Day
		4. Slot on Day
		5. Session Type
		6. Possible - all the possible assignments that the heuristics have calculated, in case of
			backtrack will be used as other options and delete the one from the list
			which is the current assignment
		7. Index - the index of the current assignment in the possible list to delete on backtrack
			and not re-use it again on subsequent backtrack calls
	It also stores the previous and next nodes respectively.
	When the current node's possible list gets exhausted and still has to backtrack then the previous
	node is taken into consideration and then run accordingly.
'''
class Node:
	def __init__(self, module, tutor, day, slot, sessionType, possible, index):
		self.assignment = [module, tutor, day, slot, sessionType]
		self.possible = possible
		self.index = index
		self.prev = None
		self.next = None
'''
	This is the structure to store the nodes so that the analysis of the current assignments
	for backtrack or to assign the final timetable structure is done.
	Stores the root to indicate the start of the tree
	Stores the leaf to indicate the latest/current state of the tree.
'''

class Tree:
	def __init__(self):
		self.root = None
		self.leaf = None
	'''
		Adds the new node into the tree by updating the leaf's next and prev respectively.
		If it is the first node then updating the root and leaf respectively.
	'''
	def add(self, node):
		if(self.root == None):
			self.root = node
			self.leaf = node
		else:
			node.prev = self.leaf
			self.leaf.next = node
			self.leaf = node
	'''
		Removes the node from the tree there by updating the leaf/root accordingly.
		If there is no leaf indicates that the tree is empty and there's nothing to 
		removed. 
		Else, the leaf's prev and next are updating accordingly. 
	'''
	def remove(self):
		if self.leaf == None:
			return None
		else:
			old = self.leaf
			self.leaf = old.prev
			self.leaf.next = None
			return old

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
	'''
		This returns a dict of the the legal domains of the given values.
		Namely - modules, tutors, days, slots.
	'''
	def domains(self, slots, modules, tutors):
		return {"modules": modules, 
				"tutors": tutors, 
				"days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], 
				"slots": slots}
	# choosing the module with minimum tutors available (tutors are dynamically updated in all the places)
	'''
		This is the heuristic function that is used for Task 1 - createSchedule()
		From the module domain it generates a list of all the modules which have 
		gotten the least number of tutors. From this list along with the list of tutors for each module, 
		the modules are filtered by the tutors having the maximum 
		number of days available. This list is passed to the method slotCheck() which checks whether
		the available days of the tutors selected for the respective modules 
		have got the required slots and if they do, adds it to the possible days.
		From this possible module-tutor-days, the tuples with the days with the maximum slots 
		get selected and then returned as a list - "possible". 
	'''
	def moduleChoose(self, moduleDomain, tutorDomain, slotDomain):
		minTutors = math.inf
		minModule = {}
		# Choosing the modules with the least tutors available
		for module in moduleDomain:
			if self.tutorListLength(tutorDomain, moduleDomain[module]) < minTutors:
				minModule.clear()
				minModule[module] = moduleDomain[module]
				minTutors = self.tutorListLength(tutorDomain, moduleDomain[module]) 
			elif len(moduleDomain[module]) == minTutors:
				minModule[module] = moduleDomain[module]
		# From the modules chosen along with the tutors, choosing the tutor with the max available days
		# which implies the max available slots because for this task a tutor can only teach a single
		# module a day
		selected = {}
		maxDays = -1
		for module in minModule:
			for tutor in minModule[module]:
				if len(tutorDomain[tutor][0]) > maxDays and tutorDomain[tutor][1] - 1 >= 0:
					selected.clear()
					selected[module] = []
					selected[module].append(tutor)
					maxDays = len(tutorDomain[tutor][0])
				elif len(tutorDomain[tutor][0]) == maxDays and tutorDomain[tutor][1] - 1 >= 0:
					if module in selected:
						selected[module].append(tutor)
					else:
						selected[module] = []
						selected[module].append(tutor)

		# From the selected pairs, the list is passed to this method to check
		# whose days match with the available days in the slotDomain
		slotsAssigned = self.slotCheck(slotDomain, tutorDomain, selected)
		
		# From these filtered tuples, the days with the maximum slots get put into the final 
		# list which is returned to the task scheduler out of which the first one is taken
		# into consideration and the remaining are put into the possibles in the node
		# which on backtrack can be used accordingly.
		possible = self.maxSlots(slotsAssigned, slotDomain)
		return possible

	'''
		This method is predominantly used for Task 3. It checks whether the given assignment
		has been deduced by the Tutor's best days or not. If it is the best days then out of the days
		chosen the days with the minimum slots are chosen and appended to the list.
		Otherwise the days with the maximum slots are chosen and appended to the list
	'''
	def minSlots(self, slotsAssigned, slotDomain):
		minSlots = math.inf
		maxSlots = -1
		possible = []
		try:
			for slots in slotsAssigned:
				# In the slots checking the variable which stores True if the
				# best days of the tutor are chosen and False otherwise.
				if slotsAssigned[slots][2]:
					# Checking for the Minimum slots if True
					for days in slotsAssigned[slots][1]:
						if slotDomain[days] < minSlots:
							possible = []
							minSlots = slotDomain[days]
							assignment = [slots, slotsAssigned[slots][0], days, slotsAssigned[slots][2]]
							possible.append(assignment)
						elif slotDomain[days] == minSlots:
							assignment = [slots, slotsAssigned[slots][0], days, slotsAssigned[slots][2]]
							possible.append(assignment)
				# Checking for the maximum slots if False
				else:
					for days in slotsAssigned[slots][1]:
						if slotDomain[days] > maxSlots:
							possible = []
							maxSlots = slotDomain[days]
							assignment = [slots, slotsAssigned[slots][0], days, slotsAssigned[slots][2]]
							possible.append(assignment)
						elif slotDomain[days] == maxSlots:
							assignment = [slots, slotsAssigned[slots][0], days, slotsAssigned[slots][2]]
							possible.append(assignment)
		except:
			return None
		return possible
	'''
		From the given argument (mainly concerned with days) referring the slotDomain
		filters the ones with the maximum slots available and then appends it to the 
		list being returned.
	'''
	def maxSlots(self, slotsAssigned, slotDomain):
		maxSlots = -1
		possible = []
		try:
			# iterating through the given list and checking the respective days for each individual possible 
			# assignment. If it is a max or equals the max number of slots. 
			for slots in slotsAssigned:
				for days in slotsAssigned[slots][1]:
					if slotDomain[days] > maxSlots:
						possible = []
						maxSlots = slotDomain[days]
						assignment = [slots, slotsAssigned[slots][0], days]
						possible.append(assignment)
					elif slotDomain[days] == maxSlots:
						assignment = [slots, slotsAssigned[slots][0], days]
						possible.append(assignment)
		except:
			return None
		return possible
	'''
		From the selected assignments with the possible days, add/filter the days
		which align with the present slotDomain, i.e. which allow a legal assignment
		and not assigning more than 1 to any slot.
	'''
	def slotCheck(self, slotDomain, tutorDomain, selected):
		available = {}
		found = False
		for module in selected:
			available[module] = {}
			for tutor in selected[module]:
				days = []
				# for all the available days in the slot domain
				for day in slotDomain:
					# if the slotDomain's day is available in the tutor's domain
					# then append the day with the possible assignments.
					if day in tutorDomain[tutor][0]:
						days.append(day)
						found = True
				if found:
					available[module] = [tutor, days]
		# a dict of modules: and tutors with days available
		return available

	'''
		This is a sub-heuristic function used by Task 3's heuristic function. When checking whether
		the selected Tutors day align with the available slots in the slotDomain, out of the selected days
		if the best days of the tutor (module or lab) intersect with it, then the intersecting set is passed
		as the day set setting the flag as True so that out of these days the days with the minimum slots are
		chosen.
	'''
	def slotCheckMinCost(self, slotDomain, tutorDomain, selected):
		available = {}
		found = False
		for module in selected:
			available[module] = {}
			for tutor in selected[module]:
				days = []
				# for all the available days in the slot domain
				for day in slotDomain:
					# if the slotDomain's day is available in the tutor's domain
					# then append the day with the possible assignments.
					if day in tutorDomain[tutor[0]][0]:
						if tutor[1] == "module":
							if tutorDomain[tutor[0]][0][day] - 2 >= 0:
								days.append(day)
								found = True
						elif tutor[1] == "lab":
							if tutorDomain[tutor[0]][0][day] - 1 >= 0:
								days.append(day)
								found = True
				if found:
					if tutor[1] == "module":
						# Checking if the tutor's best days intersect, True is to indicate 
						# that its a module and need the best days for the modules
						if list(set(days) & set(self.nextDays(tutor[0], tutorDomain, True))):
							available[module] = [tutor, list(set(days) & set(self.nextDays(tutor[0], tutorDomain, True))), True]
						else:
							available[module] = [tutor, days, False]
					if tutor[1] == "lab":
						# Checking if the tutor's best days intersect, False is to indicate 
						# that its a Lab and need the best days for the labs
						if list(set(days) & set(self.nextDays(tutor[0], tutorDomain, False))):
							available[module] = [tutor, list(set(days) & set(self.nextDays(tutor[0], tutorDomain, False))), True]
						else:
							available[module] = [tutor, days, False]
		# a dict of modules: and tutors with days available
		return available

	'''
		This is a sorting method which is used to sort the list of tutors according to their
		number of topics in their respective expertise. This is done so that as a tie-breaker
		when it comes down to the wire, the tutors with a lesser number of topics get picked 
		leaving the ones with more topics so that they might be used elsewhere.
		This uses mergeSort technique.
	'''
	def mergeSortTutors(self, tutors):
		if len(tutors)>1:
			mid = len(tutors)//2
			lefthalf = tutors[:mid]
			righthalf = tutors[mid:]

			self.mergeSortTutors(lefthalf)
			self.mergeSortTutors(righthalf)
			i=j=k=0
			while i < len(lefthalf) and j < len(righthalf):
				if len(lefthalf[i].expertise) < len(righthalf[j].expertise):
					tutors[k] = lefthalf[i]
					i+=1
				else:
					tutors[k] = righthalf[j]
					j+=1
				k+=1
			while i < len(lefthalf):
				tutors[k] = lefthalf[i]
				i+=1
				k+=1
			while j < len(righthalf):
				tutors[k] = righthalf[j]
				j+=1
				k+=1
	def mergeSortModules(self, modules):
		if len(modules)>1:
			mid = len(modules)//2
			lefthalf = modules[:mid]
			righthalf = modules[mid:]

			self.mergeSortModules(lefthalf)
			self.mergeSortModules(righthalf)
			i=j=k=0
			while i < len(lefthalf) and j < len(righthalf):
				if len(lefthalf[i].topics) > len(righthalf[j].topics):
					modules[k] = lefthalf[i]
					i+=1
				else:
					modules[k] = righthalf[j]
					j+=1
				k+=1
			while i < len(lefthalf):
				modules[k] = lefthalf[i]
				i+=1
				k+=1
			while j < len(righthalf):
				modules[k] = righthalf[j]
				j+=1
				k+=1
	'''
		This method, after assigning all the slots in the timetable, is to assign the slots stored in the nodes 
		to the timetable object. Essentially to return the final object after everything has been assigned legally.
	'''
	def assignTree(self, tree, timetableObj):
		node = tree.root
		while(node is not None):
			timetableObj.addSession(node.assignment[2], node.assignment[3], node.assignment[1], node.assignment[0], node.assignment[4])
			node = node.next

	'''
		This backtrack method is for Task 1 - createSchedule(). When this is called, it indicates
		that the present/latest assignment is not legal because the subsequent run had failed.
		So to address this the present assignment is reverted, i.e. deleted and added back to the respective
		domains. Then if the node's possible list has any more assignments that could be tested then the first
		available one is used and domains are updated accordingly. If not the present node is deleted and then
		backracks onto the previous node.
	'''
	def backtrack(self, moduleDomain, tutorDomain, slotDomain, tree):
		# Deleting the current assignment from the possible list of the node
		del tree.leaf.possible[0]
		# Re-add the module along with its eligible tutor list back into the module domain
		moduleDomain[tree.leaf.assignment[0]] = self.eligibleTutors(tree.leaf.assignment[0], True)
		# Re-add the day assigned back into the tutor's domain
		tutorDomain[tree.leaf.assignment[1]][0].append(tree.leaf.assignment[2])
		# If due to this assignment all the tutor credits have become 0, when assigning the tutor
		# would've been deleted from all the moduleDomains because he/she would've been unavailable
		# So add it back to all the ones he/she can teach.
		if tutorDomain[tree.leaf.assignment[1]][1] == 0:
			for module in moduleDomain:
				if self.tutorCanTeach(tree.leaf.assignment[1], module, True):
					moduleDomain[module].append(tree.leaf.assignment[1]) 
		# Add the credit back to him
		tutorDomain[tree.leaf.assignment[1]][1] +=1
		# If the day assigned is in the slot domain, add it otherwise create it and assign 1
		if tree.leaf.assignment[2] in slotDomain:
			slotDomain[tree.leaf.assignment[2]] +=1
		else:
			slotDomain[tree.leaf.assignment[2]] = 1
		
		# If the possible list of the node has elements, assign the first available one and update domains.
		if (tree.leaf.possible):
			tree.leaf.assignment[0] = tree.leaf.possible[0][0]
			tree.leaf.assignment[1] = tree.leaf.possible[0][1]
			tree.leaf.assignment[2] = tree.leaf.possible[0][2]
			tree.leaf.assignment[3] = slotDomain[tree.leaf.possible[0][2]]
			# Updating the moduleDomain, i.e. deleting the module being assigned
			del moduleDomain[tree.leaf.possible[0][0]]
			# Updating the slotDomain, i.e. subtracting a credit from the day being assigned
			# If it is 0 after subtraction then deleting the day.
			slotDomain[tree.leaf.possible[0][2]] -=1
			if(slotDomain[tree.leaf.possible[0][2]] == 0):
				del slotDomain[tree.leaf.possible[0][2]]
			# Since for this task a tutor can only teach a single module a day, 
			# deleting the day which has been assigned from the tutorDomain
			tutorDomain[tree.leaf.possible[0][1]][0].remove(tree.leaf.possible[0][2])
			# Subtracting 1 from the tutorDomain's overall credits
			tutorDomain[tree.leaf.possible[0][1]][1] -=1
			# If after subtraction, it is 0, delete this tutor from the modules in the ModuleDomain
			# which can be taught by this tutor.
			if tutorDomain[tree.leaf.possible[0][1]][1] == 0:
				for module in moduleDomain:
					if tree.leaf.possible[0][1] in moduleDomain[module]:
						moduleDomain[module].remove(tree.leaf.possible[0][1])
			return False
		else:
			tree.remove()
			return True

	'''
		This method is used to create/return a timetable object for Task 1.  
	'''
	def createSchedule(self):
		#Do not change this line
		start = time.time()
		timetableObj = timetable.Timetable(1)
		# Assigning the formal domains, with the required slots, tutors and modules.
		domain = self.domains([1,2,3,4,5], self.moduleList, self.tutorList)
		# SlotDomain to store and maintain the days with available slots
		slotDomain = {}
		for day in domain["days"]:
			slotDomain[day] = 5
		# ModuleDomain to store and maintain the list of modules with the legal tutors who are available
		moduleDomain = {}
		for module in domain["modules"]:
			moduleDomain[module] = self.eligibleTutors(module, True)
		# TutorDomain to store and maintain the list of tutors with their available days and credits
		tutorDomain = {}
		# Sorting the tutorlist in the ascending order of their to number of topics in the expertise
		self.mergeSortTutors(self.tutorList)
		for tutor in domain["tutors"]:
			tutorDomain[tutor] = [domain["days"].copy(), 2]
		tree = Tree()
		back = 0
		backtracking = False
		# Iterate until there are no modules in the moduleDomain, and assign the tree after the loop comes out
		while(moduleDomain):
			# checking if the mode isn't set to backtracking
			if not backtracking:
				# using the heuristic function for Task 1 to choose the assignment
				x = self.moduleChoose(moduleDomain, tutorDomain, slotDomain)
				# checking if the heuristic returned any valid, or set to backtrack
				if not (x == None or len(x) == 0):
					# adding this assignment along with the other possible assignments into a node and that node into a tree
					tree.add(Node(x[0][0],x[0][1],x[0][2], slotDomain[x[0][2]], "module", x, 0))
					# Updating the moduleDomain, i.e. deleting the module being assigned
					del moduleDomain[x[0][0]]
					# Updating the slotDomain, i.e. subtracting a credit from the day being assigned
					# If it is 0 after subtraction then deleting the day.
					slotDomain[x[0][2]] -=1
					if(slotDomain[x[0][2]] == 0):
						del slotDomain[x[0][2]]
					# Since for this task a tutor can only teach a single module a day, 
					# deleting the day which has been assigned from the tutorDomain
					tutorDomain[x[0][1]][0].remove(x[0][2])
					# Subtracting 1 from the tutorDomain's overall credits
					tutorDomain[x[0][1]][1] -=1
					# If after subtraction, it is 0, delete this tutor from the modules in the ModuleDomain
					# which can be taught by this tutor.
					if tutorDomain[x[0][1]][1] == 0:
						for module in moduleDomain:
							if x[0][1] in moduleDomain[module]:
								moduleDomain[module].remove(x[0][1])
				# if there are no valid assignments returned by the heuristics, set to backtrack
				else:
					back+=1
					backtracking = True
			# if backtrack is set then call backtrack method for this task
			else:
				backtracking = self.backtrack(moduleDomain, tutorDomain, slotDomain, tree)
		# after coming out of the loop, i.e. assigning all the modules-tutors-day-slots, assign the tree
		# into a TT object.
		self.assignTree(tree, timetableObj)

		end = time.time()
		print("BACKTRACK ", back)
		print("TIME ELAPSED ", end-start)
		#Do not change this line
		return timetableObj
	'''
		This method returns the count of the tutors in the tutorList passed as the parameter
		whose available credits are not 0.
	'''
	def tutorListLength(self, tutorDomain, tutorList):
		c = 0
		for tutor in tutorList:
			if tutorDomain[tutor][1] > 0:
				c+=1
		return c

	'''
		This is the heuristic function that is used for Task 2 - createLabSchedule().
		From the moduleDomain from this task - [(moduleTutors), (labTutors)] - for each 
		module, the module with the least count (any sessionType i.e. module/lab) will 
		be appended to the list. For each module both the lists (eligible tutors for the module
		and eligible tutors for the lab) are checked.
		Then from this filtered list the tutors with the maximum days are chosen. There are
		separate maximum day counters for both the sessiontypes. 
		In both these heuristics the respective session types are tagged along with the 
		selected module-tutor-days.
		Then for the selected module-tutors-days (modules with the least tutors who have
		the maximum number of days) the tutor-days are checked against the slotDomain which 
		validates and filters the ones whose slots are available and out of these 
		filtered days the days with the maximum slots are taken and returned as the result
	'''
	def moduleLabChoose(self, moduleDomain, tutorDomain, slotDomain):
		minTutors = math.inf
		minModule = {}
		# Choosing the modules with the least tutors available (module or lab sessions)
		for module in moduleDomain:
			i = 0
			while(i<len(moduleDomain[module])):
				if moduleDomain[module][i] != [None]:
					if self.tutorListLength(tutorDomain, moduleDomain[module][i]) < minTutors and len(moduleDomain[module][i]) != 0:
						minModule.clear()
						if i == 0:
							minModule[module] = (moduleDomain[module][i], "module")
							minTutors = self.tutorListLength(tutorDomain, moduleDomain[module][i])
						elif i == 1:
							minModule[module] = (moduleDomain[module][i], "lab")
							minTutors = self.tutorListLength(tutorDomain, moduleDomain[module][i])
					elif self.tutorListLength(tutorDomain, moduleDomain[module][i]) == minTutors and len(moduleDomain[module][i]) != 0:
						if i == 0:
							minModule[module] = (moduleDomain[module][i], "module")
						elif i == 1:
							minModule[module] = (moduleDomain[module][i], "lab")
				i+=1
		# From the modules chosen along with the tutors and the sessionType,
		# choosing the tutor with the min available days 
		# and checking the tutor's credits eligibility as well.
		selected = {}
		maxDaysMod = -1
		maxDaysLab = -1
		for module in minModule:
			for tutor in minModule[module][0]:
				if minModule[module][1] == "module":
					if len(tutorDomain[tutor][0]) > maxDaysMod and tutorDomain[tutor][1] - 2 >= 0:
						selected.clear()
						selected[module] = []
						selected[module].append((tutor,"module"))
						maxDaysMod = len(tutorDomain[tutor][0])
					elif len(tutorDomain[tutor][0]) == maxDaysMod and tutorDomain[tutor][1] - 2 >= 0:
						if module in selected:
							selected[module].append((tutor,"module"))
						else:
							selected[module] = []
							selected[module].append((tutor,"module"))
				if minModule[module][1] == "lab":
					if len(tutorDomain[tutor][0]) > maxDaysLab and tutorDomain[tutor][1] - 1 >= 0:
						selected.clear()
						selected[module] = []
						selected[module].append((tutor,"lab"))
						maxDaysLab = len(tutorDomain[tutor][0])
					elif len(tutorDomain[tutor][0]) == maxDaysLab and tutorDomain[tutor][1] - 1 >= 0:
						if module in selected:
							selected[module].append((tutor,"lab"))
						else:
							selected[module] = []
							selected[module].append((tutor,"lab"))
		# From the selected options/assignments filtering the ones whose tutors'
		# supposed days are available or co align with the slotDomain (i.e. that 
		# they are eligible) 
		slotsAssigned = self.slotCheckLab(slotDomain, tutorDomain, selected)
		# From the eligible days (entire options included), select the days
		# which have the maximum number of slots.
		possible = self.maxSlots(slotsAssigned, slotDomain)
		return possible	
	'''
		This is the heuristic function for Task 3 - createMinCostSchedule().
		From the moduleDomain from this task - [(moduleTutors), (labTutors)] - for each 
		module, the module with the least count (any sessionType i.e. module/lab) will 
		be appended to the list. For each module both the lists (eligible tutors for the module
		and eligible tutors for the lab) are checked.
		Then from these selected options, i.e. the tutors are filtered on the basis of who 
		is the busiest. If it is a "module" then only 'a' option is chosen from the options
		but if it is a "lab" then all the most busiest are chosen.
		Then from the selected options if the tutor's best days intersect with the days 
		available from the slotDomain, the best days are chosen as the options otherwise the
		days available. With those filtered options, if the best days are chosen then the days with
		the minimum slots are selected but if any other days are chosen then the days
		with the maximum slots. 	
	'''
	def moduleMinCost(self, moduleDomain, tutorDomain, slotDomain):
		minTutors = math.inf
		minModule = {}
		# Choosing the modules with the least tutors available (module or lab sessions)
		for module in moduleDomain:
			i = 0
			while(i<len(moduleDomain[module])):
				if moduleDomain[module][i] != [None]:
					if self.tutorListLength(tutorDomain, moduleDomain[module][i]) < minTutors and len(moduleDomain[module][i]) != 0:
						minModule.clear()
						if i == 0:
							minModule[module] = (moduleDomain[module][i], "module")
							minTutors = self.tutorListLength(tutorDomain, moduleDomain[module][i])
						elif i == 1:
							minModule[module] = (moduleDomain[module][i], "lab")
							minTutors = self.tutorListLength(tutorDomain, moduleDomain[module][i])
					elif self.tutorListLength(tutorDomain, moduleDomain[module][i]) == minTutors and len(moduleDomain[module][i]) != 0:
						if i == 0:
							minModule[module] = (moduleDomain[module][i], "module")
						elif i == 1:
							minModule[module] = (moduleDomain[module][i], "lab")
				i+=1
		# From the modules chosen along with the tutors and the sessionType, 
		# choose the ones who are the busiest 
		selected = {}
		maxMod = -1
		maxLab = -1
		for module in minModule:
			for tutor in minModule[module][0]:
				if minModule[module][1] == "module":
					if tutorDomain[tutor][3] > maxMod and tutorDomain[tutor][1] - 2 >= 0:
						selected.clear()
						selected[module] = []
						selected[module].append((tutor,"module"))
						maxMod = tutorDomain[tutor][3]
				if minModule[module][1] == "lab":
					if tutorDomain[tutor][4] > maxLab and tutorDomain[tutor][1] - 1 >= 0:
						selected.clear()
						selected[module] = []
						selected[module].append((tutor,"lab"))
						maxLab = tutorDomain[tutor][4]
					elif tutorDomain[tutor][4] == maxLab and tutorDomain[tutor][1] - 1 >= 0:
						if module in selected:
							selected[module].append((tutor,"lab"))
						else:
							selected[module] = []
							selected[module].append((tutor,"lab"))
		# From the selected options filtering out the days which aren't legal and checking if 
		# any of the days intersect with the tutor's present best days and if so put the intersection in
		slotsAssigned = self.slotCheckMinCost(slotDomain, tutorDomain, selected)
		# If the best days are used, select the day with the minimum number of slots available.
		# Otherwise maximum.
		possible = [self.minSlots(slotsAssigned, slotDomain), self.slots(self.slotCheckMinCost(slotDomain, tutorDomain, selected))]
		return possible	

	'''
		This method is used to put all the days into the options when the tutor's best 
		days are legal.
	'''
	def slots(self, slotsAssigned):
		possible = []
		try:
			for slots in slotsAssigned:
				for days in slotsAssigned[slots][1]:
					assignment = [slots, slotsAssigned[slots][0], days]
					possible.append(assignment)
		except:
			return None
		return possible
					
	'''
		From the selected assignments with the possible days, add/filter the days
		which align with the present slotDomain, i.e. which allow a legal assignment
		and not assigning more than 1 to any slot.
	'''
	def slotCheckLab(self, slotDomain, tutorDomain, selected):
		available = {}
		found = False
		for module in selected:
			available[module] = {}
			for tutor in selected[module]:
				days = []
				for day in slotDomain:
					if day in tutorDomain[tutor[0]][0]:
						# can do a list of all the days and then choosing the one with the max slots
						if tutor[1] == "module":
							if tutorDomain[tutor[0]][0][day] - 2 >= 0:
								days.append(day)
								found = True
						elif tutor[1] == "lab":
							if tutorDomain[tutor[0]][0][day] - 1 >= 0:
								days.append(day)
								found = True

				if found:
					available[module] = [tutor, days]
		# a dict of modules: and tutors with days available
		return available

	'''
		This backtrack method is for Task 2 - createLabSchedule(). When this is called, it indicates
		that the present/latest assignment is not legal because the subsequent run had failed.
		So to address this the present assignment is reverted, i.e. deleted and added back to the respective
		domains. Then if the node's possible list has any more assignments that could be tested then the first
		available one is used and domains are updated accordingly. If not the present node is deleted and then
		backracks onto the previous node.
		Updating the domains are specific and dependent on the session type been assigned currently.
	'''
	def backtrackLab(self, moduleDomain, tutorDomain, slotDomain, tree):
		index = tree.leaf.index
		# Deleting the current assignment from the possible list of the node
		del tree.leaf.possible[index]
		sessionType = tree.leaf.assignment[4]
		# Checking for the session type in order to update the domains accordingly 
		if sessionType == "module":
			# If the current module is in the module domain then re-assign the 0th element
			# to the eligible tutors, otherwise assign 2 empty lists and then assign the 1st
			# (0th element) to the eligble tutors of the module
			if tree.leaf.assignment[0] in moduleDomain:
				moduleDomain[tree.leaf.assignment[0]][0] = self.eligibleTutors(tree.leaf.assignment[0], True)
			else :
				moduleDomain[tree.leaf.assignment[0]] = [[],[]]
				moduleDomain[tree.leaf.assignment[0]][0] = self.eligibleTutors(tree.leaf.assignment[0], True)
			# If the current day is in the tutorDomains day domain then add 2
			# credits back to it, otherwise assign 2 credits to it appending.
			if tree.leaf.assignment[2] in tutorDomain[tree.leaf.assignment[1]][0]:
				tutorDomain[tree.leaf.assignment[1]][0][tree.leaf.assignment[2]] += 2
			else :
				tutorDomain[tree.leaf.assignment[1]][0][tree.leaf.assignment[2]] = 2
			# If the tutors overall credits became 1 with this assignment then add it
			# back to all the modules which can be taught (only modules because it wouldn't
			# have been deleted from the lab session domains) by this tutor
			if tutorDomain[tree.leaf.assignment[1]][1] == 1:
				for module in moduleDomain:
					if self.tutorCanTeach(tree.leaf.assignment[1], module, True):
						if moduleDomain[module][0] == [None]:
							moduleDomain[module][0] = [tree.leaf.assignment[1]]
						else:
							moduleDomain[module][0].append(tree.leaf.assignment[1])
			# If the tutors overall credits became 0 with this assignment then add it
			# back to all the modules which can be taught (mod and labs) by this tutor
			elif tutorDomain[tree.leaf.assignment[1]][1] == 0:
				for module in moduleDomain:
					if self.tutorCanTeach(tree.leaf.assignment[1], module, True):
						if moduleDomain[module][0] == [None]:
							moduleDomain[module][0] = [tree.leaf.assignment[1]]
						else:
							moduleDomain[module][0].append(tree.leaf.assignment[1]) 
					if self.tutorCanTeach(tree.leaf.assignment[1], module, False):
						if moduleDomain[module][1] == [None]:
							moduleDomain[module][1] = [tree.leaf.assignment[1]]
						else:
							moduleDomain[module][1].append(tree.leaf.assignment[1]) 
			# Updating the overall credits of the tutor
			tutorDomain[tree.leaf.assignment[1]][1] +=2
		if sessionType == "lab":
			# If the current module is in the module domain then re-assign the 1st element
			# to the eligible tutors, otherwise assign 2 empty lists and then assign the 2nd
			# (1st element) to the eligble tutors of the module
			if tree.leaf.assignment[0] in moduleDomain:
				moduleDomain[tree.leaf.assignment[0]][1] = self.eligibleTutors(tree.leaf.assignment[0], False)
			else :
				moduleDomain[tree.leaf.assignment[0]] = [[],[]]
				moduleDomain[tree.leaf.assignment[0]][1] = self.eligibleTutors(tree.leaf.assignment[0], False)
			# If the current day is in the tutorDomains day domain then add 2
			# credits back to it, otherwise assign 2 credits to it appending.
			if tree.leaf.assignment[2] in tutorDomain[tree.leaf.assignment[1]][0]:
				tutorDomain[tree.leaf.assignment[1]][0][tree.leaf.assignment[2]] += 1
			else :
				tutorDomain[tree.leaf.assignment[1]][0][tree.leaf.assignment[2]] = 1			
			# If the tutors overall credits became 0 with this assignment then add it
			# back to all the modules which can be taught (only labs because on re-adding
			# this credit, it will only be 1 which isn't sufficent to teach a module) by this tutor
			if tutorDomain[tree.leaf.assignment[1]][1] == 0:
				for module in moduleDomain:
					if self.tutorCanTeach(tree.leaf.assignment[1], module, False):
						if moduleDomain[module][1] == [None]:
							moduleDomain[module][1] = [tree.leaf.assignment[1]]
						else:
							moduleDomain[module][1].append(tree.leaf.assignment[1])
			# Updating the overall credits of the tutor
			tutorDomain[tree.leaf.assignment[1]][1] +=1
		# If the day assigned currently is in the slotDomain
		# then add the slot count back to it otherwise assign 1 to it.
		if tree.leaf.assignment[2] in slotDomain:
			slotDomain[tree.leaf.assignment[2]] +=1
		else:
			slotDomain[tree.leaf.assignment[2]] = 1
		
		# If the possible list of the node has elements, assign the first available one and update domains.
		if (tree.leaf.possible):
			newIndex = 0
			session = tree.leaf.possible[newIndex][1][1]
			tree.leaf.assignment[0] = tree.leaf.possible[newIndex][0]
			tree.leaf.assignment[1] = tree.leaf.possible[newIndex][1][0]
			tree.leaf.assignment[2] = tree.leaf.possible[newIndex][2]
			tree.leaf.assignment[3] = slotDomain[tree.leaf.possible[newIndex][2]]
			tree.leaf.assignment[4] = session
			tree.leaf.index = newIndex
			# checking the sessiontype been assigned to update the domains accordingly
			if session == "module":
				# Since its a module, assigning an empty set to it (0th) indicating that the
				# module session has been fulfilled for this module
				moduleDomain[tree.leaf.possible[newIndex][0]][0] = []
				# Checking if the lab session is also fulfilled (if its an empty set)
				# if so, then deleting the module from the moduleDomain
				if len(moduleDomain[tree.leaf.possible[newIndex][0]][1]) == 0:
					del moduleDomain[tree.leaf.possible[newIndex][0]]
				# Updating the day slots for the day been assigned
				slotDomain[tree.leaf.possible[newIndex][2]] -= 1
				# If after updating the day slots, the day's remaining slots become 0
				# then it is deleted from the slotDomain
				if(slotDomain[tree.leaf.possible[newIndex][2]] == 0):
					del slotDomain[tree.leaf.possible[newIndex][2]]
				# Updating the tutor's day credits in the tutorDomain
				tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]] -=2
				# If the day credits equal to 0 then delete the day from the tutorDays
				if tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]] == 0:
					del tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]]
				# Updating the overall credits of the tutor in the tutordomain
				tutorDomain[tree.leaf.possible[newIndex][1][0]][1] -=2
			if session == "lab":
				# Since its a module, assigning an empty set to it (1st) indicating that the
				# lab session has been fulfilled for this module
				moduleDomain[tree.leaf.possible[newIndex][0]][1] = []
				# Checking if the module session is also fulfilled (if 1st element is an empty set)
				# if so, then deleting the module from the moduleDomain
				if len(moduleDomain[tree.leaf.possible[newIndex][0]][0]) == 0:
					del moduleDomain[tree.leaf.possible[newIndex][0]]
				# Updating the day slots for the day been assigned
				slotDomain[tree.leaf.possible[newIndex][2]] -= 1
				# If after updating the day slots, the day's remaining slots become 0
				# then it is deleted from the slotDomain
				if(slotDomain[tree.leaf.possible[newIndex][2]] == 0):
					del slotDomain[tree.leaf.possible[newIndex][2]]
				# Updating the tutor's day credits in the tutorDomain
				tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]] -=1
				# If the day credits equal to 0 then delete the day from the tutorDays
				if tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]] == 0:
					del tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]]
				# Updating the overall credits of the tutor in the tutordomain
				tutorDomain[tree.leaf.possible[newIndex][1][0]][1] -=1
			# If after updating the overall credits of the tutor, they are 0
			# then deleting it from all the modules where it is eligible because
			# the tutor isn't available anymore.
			if tutorDomain[tree.leaf.possible[newIndex][1][0]][1] == 1:
				for module in moduleDomain:
					if tree.leaf.possible[newIndex][1][0] in moduleDomain[module][0]:
						moduleDomain[module][0].remove(tree.leaf.possible[newIndex][1][0])
						if moduleDomain[module][0] == []:
							moduleDomain[module][0] = [None] 
			elif tutorDomain[tree.leaf.possible[newIndex][1][0]][1] == 0:
				for module in moduleDomain:
					if tree.leaf.possible[newIndex][1][0] in moduleDomain[module][0]:
						moduleDomain[module][0].remove(tree.leaf.possible[newIndex][1][0]) 
						if moduleDomain[module][0] == []:
							moduleDomain[module][0] = [None] 
					if tree.leaf.possible[newIndex][1][0] in moduleDomain[module][1]:
						moduleDomain[module][1].remove(tree.leaf.possible[newIndex][1][0])
						if moduleDomain[module][1] == []:
							moduleDomain[module][1] = [None] 
			return False
		else:
			tree.remove()
			return True
	'''
		This backtrack method is for Task 3 - createMinCostSchedule(). When this is called, it indicates
		that the present/latest assignment is not legal because the subsequent run had failed.
		So to address this the present assignment is reverted, i.e. deleted and added back to the respective
		domains. Then if the node's possible list has any more assignments that could be tested then the first
		available one is used and domains are updated accordingly. If not the present node is deleted and then
		backracks onto the previous node.
		Updating the domains are specific and dependent on the session type been assigned currently.
	'''
	def backtrackMinCost(self, moduleDomain, tutorDomain, slotDomain, tree):
		# print("deleting", tree.leaf.possible[0])
		index = tree.leaf.index
		# Deleting the current assignment from the possible list of the node
		del tree.leaf.possible[index]
		sessionType = tree.leaf.assignment[4]
		# Checking for the session type in order to update the domains accordingly 
		if sessionType == "module":
			# If the current module is in the module domain then re-assign the 0th element
			# to the eligible tutors, otherwise assign 2 empty lists and then assign the 1st
			# (0th element) to the eligble tutors of the module
			if tree.leaf.assignment[0] in moduleDomain:
				moduleDomain[tree.leaf.assignment[0]][0] = self.eligibleTutors(tree.leaf.assignment[0], True)
			else :
				moduleDomain[tree.leaf.assignment[0]] = [[],[]]
				moduleDomain[tree.leaf.assignment[0]][0] = self.eligibleTutors(tree.leaf.assignment[0], True)
			# If the current day is in the tutorDomains day domain then add 2
			# credits back to it, otherwise assign 2 credits to it appending.
			if tree.leaf.assignment[2] in tutorDomain[tree.leaf.assignment[1]][0]:
				tutorDomain[tree.leaf.assignment[1]][0][tree.leaf.assignment[2]] += 2
			else :
				tutorDomain[tree.leaf.assignment[1]][0][tree.leaf.assignment[2]] = 2 
			# If the tutors overall credits became 1 with this assignment then add it
			# back to all the modules which can be taught (only modules because it wouldn't
			# have been deleted from the lab session domains) by this tutor
			if tutorDomain[tree.leaf.assignment[1]][1] == 1:
				for module in moduleDomain:
					if self.tutorCanTeach(tree.leaf.assignment[1], module, True):
						if moduleDomain[module][0] == [None]:
							moduleDomain[module][0] = [tree.leaf.assignment[1]]
						else:
							moduleDomain[module][0].append(tree.leaf.assignment[1])
			# If the tutors overall credits became 0 with this assignment then add it
			# back to all the modules which can be taught (mod and labs) by this tutor
			elif tutorDomain[tree.leaf.assignment[1]][1] == 0:
				for module in moduleDomain:
					if self.tutorCanTeach(tree.leaf.assignment[1], module, True):
						if moduleDomain[module][0] == [None]:
							moduleDomain[module][0] = [tree.leaf.assignment[1]]
						else:
							moduleDomain[module][0].append(tree.leaf.assignment[1]) 
					if self.tutorCanTeach(tree.leaf.assignment[1], module, False):
						if moduleDomain[module][1] == [None]:
							moduleDomain[module][1] = [tree.leaf.assignment[1]]
						else:
							moduleDomain[module][1].append(tree.leaf.assignment[1])
			# Updating the overall credits of the tutor
			tutorDomain[tree.leaf.assignment[1]][1] +=2
			# Updating the number of modules been taught currently by the tutor
			tutorDomain[tree.leaf.assignment[1]][3] -=1
			# Updating the number of credits in the other days copy to check for best days
			tutorDomain[tree.leaf.assignment[1]][2][tree.leaf.assignment[2]] +=3
		if sessionType == "lab":
			# If the current module is in the module domain then re-assign the 1st element
			# to the eligible tutors, otherwise assign 2 empty lists and then assign the 2nd
			# (1st element) to the eligble tutors of the module
			if tree.leaf.assignment[0] in moduleDomain:
				moduleDomain[tree.leaf.assignment[0]][1] = self.eligibleTutors(tree.leaf.assignment[0], False)
			else :
				moduleDomain[tree.leaf.assignment[0]] = [[],[]]
				moduleDomain[tree.leaf.assignment[0]][1] = self.eligibleTutors(tree.leaf.assignment[0], False)
			# If the current day is in the tutorDomains day domain then add 2
			# credits back to it, otherwise assign 2 credits to it appending.
			if tree.leaf.assignment[2] in tutorDomain[tree.leaf.assignment[1]][0]:
				tutorDomain[tree.leaf.assignment[1]][0][tree.leaf.assignment[2]] += 1
			else :
				tutorDomain[tree.leaf.assignment[1]][0][tree.leaf.assignment[2]] = 1
			# If the tutors overall credits became 0 with this assignment then add it
			# back to all the modules which can be taught (only labs because on re-adding
			# this credit, it will only be 1 which isn't sufficent to teach a module) by this tutor
			if tutorDomain[tree.leaf.assignment[1]][1] == 0:
				for module in moduleDomain:
					if self.tutorCanTeach(tree.leaf.assignment[1], module, False):
						if moduleDomain[module][1] == [None]:
							moduleDomain[module][1] = [tree.leaf.assignment[1]]
						else:
							moduleDomain[module][1].append(tree.leaf.assignment[1])
			# Updating the overall credits of the tutor
			tutorDomain[tree.leaf.assignment[1]][1] +=1
			# Updating the number of labs been taught currently by this tutor
			tutorDomain[tree.leaf.assignment[1]][4] -=1
			# Updating the number of credits in the other days copy to check for best days
			tutorDomain[tree.leaf.assignment[1]][2][tree.leaf.assignment[2]] +=1
		# If the day assigned currently is in the slotDomain
		# then add the slot count back to it otherwise assign 1 to it.
		if tree.leaf.assignment[2] in slotDomain:
			slotDomain[tree.leaf.assignment[2]] +=1
		else:
			slotDomain[tree.leaf.assignment[2]] = 1
		
		# If the possible list of the node has elements, assign the first available one and update domains.
		if (tree.leaf.possible):
			newIndex = self.searchPossible(tree.leaf.possible)
			session = tree.leaf.possible[newIndex][1][1]
			tree.leaf.assignment[0] = tree.leaf.possible[newIndex][0]
			tree.leaf.assignment[1] = tree.leaf.possible[newIndex][1][0]
			tree.leaf.assignment[2] = tree.leaf.possible[newIndex][2]
			tree.leaf.assignment[3] = slotDomain[tree.leaf.possible[newIndex][2]]
			tree.leaf.assignment[4] = session
			tree.leaf.index = newIndex
			# checking the sessiontype been assigned to update the domains accordingly
			if session == "module":
				# Since its a module, assigning an empty set to it (0th) indicating that the
				# module session has been fulfilled for this module
				moduleDomain[tree.leaf.possible[newIndex][0]][0] = []
				# Checking if the lab session is also fulfilled (if its an empty set)
				# if so, then deleting the module from the moduleDomain
				if len(moduleDomain[tree.leaf.possible[newIndex][0]][1]) == 0:
					del moduleDomain[tree.leaf.possible[newIndex][0]]
				# Updating the day slots for the day been assigned
				slotDomain[tree.leaf.possible[newIndex][2]] -= 1
				# If after updating the day slots, the day's remaining slots become 0
				# then it is deleted from the slotDomain
				if(slotDomain[tree.leaf.possible[newIndex][2]] == 0):
					del slotDomain[tree.leaf.possible[newIndex][2]]
				# Updating the tutor's day credits in the tutorDomain
				tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]] -=2
				# If the day credits equal to 0 then delete the day from the tutorDays
				if tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]] == 0:
					del tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]]
				# Updating the overall credits of the tutor in the tutordomain
				tutorDomain[tree.leaf.possible[newIndex][1][0]][1] -=2
				# Updating the number of modules been taught by the tutor (adding 1)
				tutorDomain[tree.leaf.possible[newIndex][1][0]][3] +=1
				# Updating the number of credits of the day been taught by the tutor (adding 3) for heuristic purposes
				tutorDomain[tree.leaf.possible[newIndex][1][0]][2][tree.leaf.possible[newIndex][2]] -=3
			if session == "lab":
				# Since its a module, assigning an empty set to it (1st) indicating that the
				# lab session has been fulfilled for this module
				moduleDomain[tree.leaf.possible[newIndex][0]][1] = []
				# Checking if the module session is also fulfilled (if 1st element is an empty set)
				# if so, then deleting the module from the moduleDomain
				if len(moduleDomain[tree.leaf.possible[newIndex][0]][0]) == 0:
					del moduleDomain[tree.leaf.possible[newIndex][0]]
				# Updating the day slots for the day been assigned
				slotDomain[tree.leaf.possible[newIndex][2]] -= 1
				# If after updating the day slots, the day's remaining slots become 0
				# then it is deleted from the slotDomain
				if(slotDomain[tree.leaf.possible[newIndex][2]] == 0):
					del slotDomain[tree.leaf.possible[newIndex][2]]
				# Updating the tutor's day credits in the tutorDomain
				tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]] -=1
				# If the day credits equal to 0 then delete the day from the tutorDays
				if tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]] == 0:
					del tutorDomain[tree.leaf.possible[newIndex][1][0]][0][tree.leaf.possible[newIndex][2]]
				# Updating the overall credits of the tutor in the tutordomain
				tutorDomain[tree.leaf.possible[newIndex][1][0]][1] -=1
				# Updating the number of labs been taught by the tutor (Adding 1)
				tutorDomain[tree.leaf.possible[newIndex][1][0]][4] +=1
				# Updating the number of credits been taught by the tutor on the day (for heuristic purposes)
				tutorDomain[tree.leaf.possible[newIndex][1][0]][2][tree.leaf.possible[newIndex][2]] -=1
			# If after updating the overall credits of the tutor, they are 0
			# then deleting it from all the modules where it is eligible because
			# the tutor isn't available anymore.
			if tutorDomain[tree.leaf.possible[newIndex][1][0]][1] == 1:
				for module in moduleDomain:
					if tree.leaf.possible[newIndex][1][0] in moduleDomain[module][0]:
						moduleDomain[module][0].remove(tree.leaf.possible[newIndex][1][0]) 
			elif tutorDomain[tree.leaf.possible[newIndex][1][0]][1] == 0:
				for module in moduleDomain:
					if tree.leaf.possible[newIndex][1][0] in moduleDomain[module][0]:
						moduleDomain[module][0].remove(tree.leaf.possible[newIndex][1][0]) 
					if tree.leaf.possible[newIndex][1][0] in moduleDomain[module][1]:
						moduleDomain[module][1].remove(tree.leaf.possible[newIndex][1][0])
				
			return False
		else:
			tree.remove()
			return True

	#Now, we have introduced lab sessions. Each day now has ten sessions, and there is a lab session as well as a module session.
	#All module and lab sessions must be assigned to a slot, and each module and lab session require a tutor.
	#The tutor does not need to be the same for the module and lab session.
	#A tutor can teach a lab session if their expertise includes at least one topic covered by the module.
	#We are now concerned with 'credits'. A tutor can teach a maximum of 4 credits. Lab sessions are 1 credit, module sessiosn are 2 credits.
	#A tutor cannot teach more than 2 credits a day.
	'''
		This method is used to create/return a timetable object for task 2.
	'''
	def createLabSchedule(self):
		#Do not change this line
		start = time.time()
		#Here is where you schedule your timetable
		timetableObj = timetable.Timetable(2)
		# Assigning the formal domains, with the required slots, tutors and modules.
		domain = self.domains([1,2,3,4,5,6,7,8,9,10], self.moduleList, self.tutorList)
		# SlotDomain to store and maintain the days with available slots
		slotDomain = {}
		for day in domain["days"]:
			slotDomain[day] = 10
		# ModuleDomain to store and maintain the list of modules with the legal tutors who are available
		moduleDomain = {}
		for module in domain["modules"]:
			moduleDomain[module] = [self.eligibleTutors(module, True), self.eligibleTutors(module, False)]
		# TutorDomain to store and maintain the list of tutors with their available days and credits
		tutorDomain = {}
		# Sorting the tutorlist in the ascending order of their to number of topics in the expertise
		self.mergeSortTutors(self.tutorList)
		dayCredits = {}
		for day in domain["days"]:
			dayCredits[day] = 2
		for tutor in domain["tutors"]:
			tutorDomain[tutor] = [dayCredits.copy(), 4]
		tree = Tree()
		back = 0
		backtracking = False
		# Iterate until there are no modules in the moduleDomain, and assign the tree after the loop comes out
		while(moduleDomain):
			# checking if the mode isn't set to backtracking
			if not backtracking:
				# using the heuristic function for Task 2 to choose the assignment
				x = self.moduleLabChoose(moduleDomain, tutorDomain, slotDomain)
				# checking if the heuristic returned any valid, or set to backtrack
				if not (x == None or len(x) == 0):
					index = 0
					sessionType = x[index][1][1]
					# adding this assignment along with the other possible assignments into a node and that node into a tree
					tree.add(Node(x[index][0],x[index][1][0],x[index][2], slotDomain[x[index][2]],sessionType, x, index))
					# checking the sessiontype been assigned to update the domains accordingly
					if sessionType == "module":
						# Since its a module, assigning an empty set to it (0th) indicating that the
						# module session has been fulfilled for this module
						moduleDomain[x[index][0]][0] = []
						# Checking if the lab session is also fulfilled (if its an empty set)
						# if so, then deleting the module from the moduleDomain
						if len(moduleDomain[x[index][0]][1]) == 0:
							del moduleDomain[x[index][0]]
						# Updating the day slots for the day been assigned
						slotDomain[x[index][2]] -= 1
						# If after updating the day slots, the day's remaining slots become 0
						# then it is deleted from the slotDomain
						if(slotDomain[x[index][2]] == 0):
							del slotDomain[x[index][2]]
						# Updating the tutor's day credits in the tutorDomain
						tutorDomain[x[index][1][0]][0][x[index][2]] -=2
						# If the day credits equal to 0 then delete the day from the tutorDays
						if tutorDomain[x[index][1][0]][0][x[index][2]] == 0:
							del tutorDomain[x[index][1][0]][0][x[index][2]]
						# Updating the overall credits of the tutor in the tutordomain
						tutorDomain[x[index][1][0]][1] -=2
					if sessionType == "lab":
						# Since its a module, assigning an empty set to it (1st) indicating that the
						# lab session has been fulfilled for this module
						moduleDomain[x[index][0]][1] = []
						# Checking if the module session is also fulfilled (if 1st element is an empty set)
						# if so, then deleting the module from the moduleDomain
						if len(moduleDomain[x[index][0]][0]) == 0:
							del moduleDomain[x[index][0]]
						# Updating the day slots for the day been assigned
						slotDomain[x[index][2]] -= 1
						# If after updating the day slots, the day's remaining slots become 0
						# then it is deleted from the slotDomain
						if(slotDomain[x[index][2]] == 0):
							del slotDomain[x[index][2]]
						# Updating the tutor's day credits in the tutorDomain
						tutorDomain[x[index][1][0]][0][x[index][2]] -=1
						# If the day credits equal to 0 then delete the day from the tutorDays
						if tutorDomain[x[index][1][0]][0][x[index][2]] == 0:
							del tutorDomain[x[index][1][0]][0][x[index][2]]
						# Updating the overall credits of the tutor in the tutordomain
						tutorDomain[x[index][1][0]][1] -=1
					# If after updating the overall credits of the tutor, they are 1
					# then deleting it from all the modules (only modules) where it is eligible because
					# the tutor isn't available anymore.
					if tutorDomain[x[index][1][0]][1] == 1:
						for module in moduleDomain:
							if x[index][1][0] in moduleDomain[module][0]:
								moduleDomain[module][0].remove(x[index][1][0])
								if moduleDomain[module][0] == []:
									moduleDomain[module][0] = [None]
					# If after updating the overall credits of the tutor, they are 0
					# then deleting it from all the modules (modules and labs) where it is eligible because
					# the tutor isn't available anymore.
					elif tutorDomain[x[index][1][0]][1] == 0:
						for module in moduleDomain:
							if x[index][1][0] in moduleDomain[module][0]:
								moduleDomain[module][0].remove(x[index][1][0])
								if moduleDomain[module][0] == []:
									moduleDomain[module][0] = [None]
							if x[index][1][0] in moduleDomain[module][1]:
								moduleDomain[module][1].remove(x[index][1][0])
								if moduleDomain[module][1] == []:
									moduleDomain[module][1] = [None]
				# if there are no valid assignments returned by the heuristics, set to backtrack
				else:
					backtracking = True
			# if backtrack is set then call backtrack method for this task
			else:
				back+=1
				if back >= 100000:
					random.shuffle(self.moduleList)
					random.shuffle(self.tutorList)
					self.mergeSortModules(self.moduleList)
					return self.createLabSchedule()
				backtracking = self.backtrackLab(moduleDomain, tutorDomain, slotDomain, tree)
		# after coming out of the loop, i.e. assigning all the modules-tutors-day-slots, assign the tree
		# into a TT object.
		self.assignTree(tree, timetableObj)

		end = time.time()
		print("BACKTRACK ", back)
		print("TIME ELAPSED ", end-start)

		#This line generates a random timetable, that may not be valid. You can use this or delete it.		
		# self.randomModAndLabSchedule(timetableObj)

		#Do not change this line
		return timetableObj

	'''
		This is a method to return the day after a given day
	'''
	def dayAfter(self, day):
		days = {"Monday":"Tuesday", "Tuesday":"Wednesday", "Wednesday":"Thursday", "Thursday":"Friday", "Friday":"Monday"}
		return days[day]

	'''
		This is a method to return the day before a given day
	'''
	def dayBefore(self, day):
		days = {"Monday":"Friday", "Tuesday":"Monday", "Wednesday":"Tuesday", "Thursday":"Wednesday", "Friday":"Thursday"}
		return days[day]

	'''
		This is a method to return the best of the tutor based on the module
		flag - True if module, False if lab. If module then the days before and after
		are considered to best and if its a lab then the same day.
	'''
	def nextDays(self, tutor, tutorDomain, module):
		if module:
			days = []
			for day in tutorDomain[tutor][2]:
				if tutorDomain[tutor][2][day] == -1:
					if day != "Friday":
						if self.dayAfter(day) not in days:
							days.append(self.dayAfter(day))
					if day != "Monday":
						if self.dayBefore(day) not in days:
							days.append(self.dayBefore(day))
		else:
			days = []
			for day in tutorDomain[tutor][2]:
				if tutorDomain[tutor][2][day] < 2 and tutorDomain[tutor][2][day] > 0:
					days.append(day)
		return days
	'''
		This is used for task 3, returning the middle element so that the probability increases 
		on backtrack. The middle element is only chosen when the length of the possible is more than 5
		because then the wide range of other possiblities with a hint of randmomness exist in case
		of backtrack
	'''
	def searchPossible(self, possible):
		if len(possible) < 5:
			return 0
		else:
			return math.ceil(len(possible)/2)
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
		start = time.time()
		#Here is where you schedule your timetable
		timetableObj = timetable.Timetable(2)
		# Assigning the formal domains, with the required slots, tutors and modules.
		domain = self.domains([1,2,3,4,5,6,7,8,9,10], self.moduleList, self.tutorList)
		# SlotDomain to store and maintain the days with available slots
		slotDomain = {}
		for day in domain["days"]:
			slotDomain[day] = 10
		# ModuleDomain to store and maintain the list of modules with the legal tutors who are available
		moduleDomain = {}
		for module in domain["modules"]:
			moduleDomain[module] = [self.eligibleTutors(module, True), self.eligibleTutors(module, False)]
		# TutorDomain to store and maintain the list of tutors with their available days and credits
		tutorDomain = {}
		# Sorting the tutorlist in the ascending order of their to number of topics in the expertise
		self.mergeSortTutors(self.tutorList)
		dayCredits = {}
		for day in domain["days"]:
			dayCredits[day] = 2
		# tutor domain (2) -> if the value is 0 means that its been occupied by a module, if no day then labs		
		# tutordomain(3) -> no of modules (4) -> no of labs
		for tutor in domain["tutors"]:
			tutorDomain[tutor] = [dayCredits.copy(), 4, dayCredits.copy(), 0, 0]
		tree = Tree()
		back = 0
		backtracking = False
		# Iterate until there are no modules in the moduleDomain, and assign the tree after the loop comes out
		while(moduleDomain):
			# checking if the mode isn't set to backtracking
			if not backtracking:
				# using the heuristic function for Task 2 to choose the assignment
				result = self.moduleMinCost(moduleDomain, tutorDomain, slotDomain)
				x = result[0]
				# checking if the heuristic returned any valid, or set to backtrack
				if not (x == None or len(x) == 0):
					# need to start from here by generalising the session type and retrieving it from tutor[0][1]
					index = self.searchPossible(x)
					sessionType = x[index][1][1]
					# If the current assignment is based on the best days then add the possible solutions
					# of the best days otherwise the normal possibles would be chosen.
					if x[index][3]:
						tree.add(Node(x[index][0],x[index][1][0],x[index][2], slotDomain[x[index][2]],sessionType, result[1], index))
					else:
						tree.add(Node(x[index][0],x[index][1][0],x[index][2], slotDomain[x[index][2]],sessionType, result[0], index))

					if sessionType == "module":
						# Since its a module, assigning an empty set to it (0th) indicating that the
						# module session has been fulfilled for this module
						moduleDomain[x[index][0]][0] = []
						# Checking if the lab session is also fulfilled (if its an empty set)
						# if so, then deleting the module from the moduleDomain
						if len(moduleDomain[x[index][0]][1]) == 0:
							del moduleDomain[x[index][0]]
						# Updating the day slots for the day been assigned
						slotDomain[x[index][2]] -= 1
						# If after updating the day slots, the day's remaining slots become 0
						# then it is deleted from the slotDomain
						if(slotDomain[x[index][2]] == 0):
							del slotDomain[x[index][2]]
						# Updating the tutor's day credits in the tutorDomain
						tutorDomain[x[index][1][0]][0][x[index][2]] -=2
						# If the day credits equal to 0 then delete the day from the tutorDays
						if tutorDomain[x[index][1][0]][0][x[index][2]] == 0:
							del tutorDomain[x[index][1][0]][0][x[index][2]]
						# Updating the overall credits of the tutor in the tutordomain
						tutorDomain[x[index][1][0]][1] -=2
						# Updating the number of modules been taught by the tutor (adding 1)
						tutorDomain[x[index][1][0]][3] +=1
						# Updating the number of credits of the day been taught by the tutor (adding 3) for heuristic purposes
						tutorDomain[x[index][1][0]][2][x[index][2]] -=3
					if sessionType == "lab":
						# Since its a module, assigning an empty set to it (1st) indicating that the
						# lab session has been fulfilled for this module
						moduleDomain[x[index][0]][1] = []
						# Checking if the module session is also fulfilled (if 1st element is an empty set)
						# if so, then deleting the module from the moduleDomain
						if len(moduleDomain[x[index][0]][0]) == 0:
							del moduleDomain[x[index][0]]
						# Updating the day slots for the day been assigned
						slotDomain[x[index][2]] -= 1
						# If after updating the day slots, the day's remaining slots become 0
						# then it is deleted from the slotDomain
						if(slotDomain[x[index][2]] == 0):
							del slotDomain[x[index][2]]
						# Updating the tutor's day credits in the tutorDomain
						tutorDomain[x[index][1][0]][0][x[index][2]] -=1
						# If the day credits equal to 0 then delete the day from the tutorDays
						if tutorDomain[x[index][1][0]][0][x[index][2]] == 0:
							del tutorDomain[x[index][1][0]][0][x[index][2]]
						# Updating the overall credits of the tutor in the tutordomain
						tutorDomain[x[index][1][0]][1] -=1
						# Updating the number of labs been taught by the tutor (Adding 1)
						tutorDomain[x[index][1][0]][4] +=1
						# Updating the number of credits been taught by the tutor on the day (for heuristic purposes)
						tutorDomain[x[index][1][0]][2][x[index][2]] -=1
					# If after updating the overall credits of the tutor, they are 1
					# then deleting it from all the modules (only modules) where it is eligible because
					# the tutor isn't available anymore.
					if tutorDomain[x[index][1][0]][1] == 1:
						for module in moduleDomain:
							if x[index][1][0] in moduleDomain[module][0]:
								moduleDomain[module][0].remove(x[index][1][0])
								if moduleDomain[module][0] == []:
									moduleDomain[module][0] = [None]
					# If after updating the overall credits of the tutor, they are 0
					# then deleting it from all the modules (modules and labs) where it is eligible because
					# the tutor isn't available anymore.
					elif tutorDomain[x[index][1][0]][1] == 0:
						for module in moduleDomain:
							if x[index][1][0] in moduleDomain[module][0]:
								moduleDomain[module][0].remove(x[index][1][0])
								if moduleDomain[module][0] == []:
									moduleDomain[module][0] = [None]
							if x[index][1][0] in moduleDomain[module][1]:
								moduleDomain[module][1].remove(x[index][1][0])
								if moduleDomain[module][1] == []:
									moduleDomain[module][1] = [None]
				# if there are no valid assignments returned by the heuristics, set to backtrack
				else:
					backtracking = True
			# if backtrack is set then call backtrack method for this task
			else:
				back+=1
				if back >= 100000:
					random.shuffle(self.moduleList)
					random.shuffle(self.tutorList)
					self.mergeSortModules(self.moduleList)
					return self.createMinCostSchedule()
				backtracking = self.backtrackMinCost(moduleDomain, tutorDomain, slotDomain, tree)
		# after coming out of the loop, i.e. assigning all the modules-tutors-day-slots, assign the tree
		# into a TT object.
		self.assignTree(tree, timetableObj)

		end = time.time()
		print("BACKTRACK ", back)
		print("TIME ELAPSED ", end-start)

		#This line generates a random timetable, that may not be valid. You can use this or delete it.		
		# self.randomModAndLabSchedule(timetableObj)

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
	'''
		This method is used to return a True/False if a tutor can teach the module
		labOrModule value - 
			True to check for Modules
			False to check for Labs
	'''

	def tutorCanTeach(self, tutor, module, labOrModule):
		if labOrModule:
			return (all(x in tutor.expertise for x in module.topics))
		else:
			return (any(x in tutor.expertise for x in module.topics))

	'''
		This method is used to return a list of tutors (True for modules 
		False for Labs) who are eligible to teach the passed modules
	'''	
	def eligibleTutors(self, module, labOrModule):
		tutors = []
		for x in self.tutorList:
			if(self.tutorCanTeach(x, module, labOrModule)):
				tutors.append(x)
		return tutors		