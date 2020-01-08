import module
import math
import tutor
import ReaderWriter
import timetable
import scheduler
import os
import time
#This file allows you to test your schedulers. tt.scheduleChecker will return false if your schedule is not legal.
#It will also print a message displaying the constraint being violated by the schedule. 

#Feel free to change the problem you use to test, the example problems folder contains 8 different problems to test your schedule on.
#You may also use those text files as a template to create your own problems, that can be read in by passing the file name to the
# readRequirements method in line 16. 

#Each task of the course work has a different method that must be filled in. The schedule checker module will
#read in the task number variable of the timetable object, which is set in the schedule creation methods.

#Overall, the only changes that need to be made to this file is commenting and uncommenting the correct method call
#based on which problem you are trying to solve, and changing which problem is loaded in. 
path = "cs255-examples-master/"
count = 0
cost = 0
def task3():
	global count
	global cost
	x = [d for d in os.listdir(path)]
	for problem in x:
		if problem != ".DS_Store"  and problem != "LICENSE" and problem != "README.md" and problem != "edges":

			print(problem)
			rw = ReaderWriter.ReaderWriter()
			[tutorList, moduleList] = rw.readRequirements(path+problem)
			sch = scheduler.Scheduler(tutorList, moduleList)

			#this method will be used to create a schedule that solves task 1
			# tt = sch.createSchedule()

			#This method will be used to create a schedule that solves task 2
			# tt = sch.createLabSchedule()

			#this method will be used to create a schedule that solves task 3
			tt = sch.createMinCostSchedule()

			# print(str(tt.schedule))
			if tt.scheduleChecker(tutorList, moduleList):
				print("Schedule is legal. TASK 3")
				count+=1
				cost+=tt.cost
				print("Schedule has a cost of " + str(tt.cost))
				print("\n\n")
			else:
				print("PROBLEM")
				print(problem)
				exit()
def task2():
	x = [d for d in os.listdir(path)]
	for problem in x:
		if problem != ".DS_Store"  and problem != "LICENSE" and problem != "README.md" and problem != "edges":

			print(problem)
			rw = ReaderWriter.ReaderWriter()
			[tutorList, moduleList] = rw.readRequirements(path+problem)
			sch = scheduler.Scheduler(tutorList, moduleList)

			#this method will be used to create a schedule that solves task 1
			# tt = sch.createSchedule()

			#This method will be used to create a schedule that solves task 2
			tt = sch.createLabSchedule()

			#this method will be used to create a schedule that solves task 3
			# tt = sch.createMinCostSchedule()

			# print(str(tt.schedule))
			if tt.scheduleChecker(tutorList, moduleList):
				print("Schedule is legal. TASK 2")
				print("Schedule has a cost of " + str(tt.cost))
				print("\n\n")
			else:
				print("PROBLEM")
				print(problem)
				exit()
def task1():
	x = [d for d in os.listdir(path)]
	for problem in x:
		if problem != ".DS_Store"  and problem != "LICENSE" and problem != "README.md" and problem != "edges":

			print(problem)
			rw = ReaderWriter.ReaderWriter()
			[tutorList, moduleList] = rw.readRequirements(path+problem)
			sch = scheduler.Scheduler(tutorList, moduleList)

			#this method will be used to create a schedule that solves task 1
			tt = sch.createSchedule()

			#This method will be used to create a schedule that solves task 2
			# tt = sch.createLabSchedule()

			#this method will be used to create a schedule that solves task 3
			# tt = sch.createMinCostSchedule()

			# print(str(tt.schedule))
			if tt.scheduleChecker(tutorList, moduleList):
				print("Schedule is legal. - TASK 1")
				print("Schedule has a cost of " + str(tt.cost))
				print("\n\n")
			else:
				print("PROBLEM")
				print(problem)
				exit()
start = time.time()
# task1()
# print("\n\nTask 1 passed")
# task2()
# print("\n\nTask 2 passed")
costs = []
for i in range(1000):
	task3()
	print("\n\nTask 3 passed")
	end = time.time()
	print("\n\nTIME FOR ALL TASKS = ",end-start)
	avg = math.ceil(cost/count)
	costs.append(avg)
	print("\n AVERAGE COST ", math.ceil(cost/count))
	print("\n\nALL TESTS PASSED")
print("\nAVERAGE ", sum(costs)/len(costs) )