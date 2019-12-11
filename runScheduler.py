import module
import tutor
import ReaderWriter
import timetable
import scheduler

#This file allows you to test your schedulers. tt.scheduleChecker will return false if your schedule is not legal.
#It will also print a message displaying the constraint being violated by the schedule. 

#Feel free to change the problem you use to test, the example problems folder contains 8 different problems to test your schedule on.
#You may also use those text files as a template to create your own problems, that can be read in by passing the file name to the
# readRequirements method in line 16. 

#Each task of the course work has a different method that must be filled in. The schedule checker module will
#read in the task number variable of the timetable object, which is set in the schedule creation methods.

#Overall, the only changes that need to be made to this file is commenting and uncommenting the correct method call
#based on which problem you are trying to solve, and changing which problem is loaded in. 

rw = ReaderWriter.ReaderWriter()
[tutorList, moduleList] = rw.readRequirements("ExampleProblems/Problem1.txt")
sch = scheduler.Scheduler(tutorList, moduleList)

#this method will be used to create a schedule that solves task 1
tt = sch.createSchedule()

#This method will be used to create a schedule that solves task 2
#tt = sch.createLabSchedule()

#this method will be used to create a schedule that solves task 3
#tt = sch.createMinCostSchedule()

print(str(tt.schedule))
if tt.scheduleChecker(tutorList, moduleList):
	print("Schedule is legal.")
	print("Schedule has a cost of " + str(tt.cost))


	print(str(tt.schedule))