There are a total of six files used for this coursework. They are as follows:

scheduler.py - this module contains 3 methods, createSchedule, createLabSchedule and createMinCostSchedule. The first one must return a valid timetable object, with each day and each slot assigned. The second must return a valid timetable for the second task, which consists of ten sessions a day, and a lab and module session for each module code. The third method must return a legal schedule, that also has the lowest cost possible. The preamble of scheduler.py explains the other methods from other classes that you may used, and in addition you may only import the python math and random libraries. When you're ready to submit, this file must be renamed to yourUniID.py, e.g. 1003685.py. 


runScheduler.py - this is the file that is run to test your solution. This file will run your scheduler, test if it is legal and print out the cost. Feel free to edit line 16 to load in a different problem file, and edit the scheduler method called from createSchedule to createLabSession or createMinCostSchedule. 


There are four other files included in this coursework bundle. They have the following functions:

tutor.py - Contains the tutor class. Notably, a tutor is defined as a name and a list of expertise. While this class has a few mutator methods (setName, setExpertise, addExpertise), the only legal ways for you to use these classes is as follows:
	t.name -- Returns the name of the tutor t as a string.
	t.expertise -- Returns the expertise subjects of tutor t as a list of strings.


module.py - Contains the module class. Notably, a module is defined as a name and a list of topics. While this class has a few mutator methods (setName, setTopics, addTopic), the only legal ways for you to use this class is as follows:
	m.name -- Returns the name of module m as a string.
	m.topics -- Returns the topics covered by module m as a list of strings. 


timetable.py - Contains the timetable class. This class will be used to store the schedule you create, and a slot can be assigned a module and tutor through the 'addSession' method, as described in the preamble for schedule.py. Importantly, the only valid days of the week are Monday, Tuesday, Wednesday, Thursday and Friday and the only slot numbers that are valid are 1, 2, 3, 4, 5, 6 ,7 , 8, 9 and 10. This class also contains the method to allow you to check you schedule is legal, and is used in runScheduler.py. However, this method cannot be used by your submitted solution in the scheduler.py file. When a timetable is created, the task number is also given, so that it can check against the correct rules. The following methods can be used in your final submission:
	
	timetable.addSession(day, timeslot, tutor, module, sessionType) -- This will fill the designated timeslot(which should be a 	number) on the given day (either Monday, Tuesday, Wednesday, Thursday, Friday) with the given module and tutor. sessionType 	should be a string with the value of either 'module' or 'lab'. For task 1 all sessions should be 'module' and for tasks 2 	and 3 there should be a 'module' and a 'lab' session for each module object. 
	
	timetable.sessionAssigned(day, timeslot) -- This can be used to let you know that the given timeslot on the given day has a 	session assigned. Returns true or false.

	timetable.getSession(day, timeslot) -- Returns the [tutor, module, sessionType] list for the session. 


ReaderWriter - class for reading in the example problems, and is also capable of writing out lists of tutors and modules if you wish to create more problems to test your solution against. The use of the reader method can be see in runSchedule.py. To use the writer method it must be passed a list of tutor objects, a list of module objects and filename. The readRequirements method converts the text file it is passed into a list of tutor and module objects. 

Each file is commented, and there is a limit to the methods and attributes you can use. 

Don't forget you should be using Python3, and can test your scheduler by running the 'runScheduler' file. 

