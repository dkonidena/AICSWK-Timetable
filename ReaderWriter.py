import module
import tutor

#This is a class that is used to read in the requirements from the problem folder and convert 
#it into a list of tutors and modules

class ReaderWriter:
	
	#This converts a text file into a list of tutors and modules, so that they can be fit to a schedule
	#Each line in the text file is a comma separated list of attributes
	def readRequirements(self,filename):
		tutorList = list()
		moduleList = list()
		with open(filename) as f:
			modules = False
			for line in f:
				#tutors are listed first, up until the breaker character, '==='
				if "===" in line:
					modules = True
				else:
					line = line.replace("\n","")
					line = line.split(",")
					#dealing with a tutor, their name is the first element in the list and the rest
					#are expertises of the tutor
					if not modules:
						expertise = list()
						for i in range(1,len(line)):
							expertise.append(line[i])
						tut = tutor.Tutor(name=line[0], expertise=expertise)
						tutorList.append(tut)
					else:
						#with modules, the code is the first element of the list, and the topics the rest
						topics = list()
						for i in range(1,len(line)):
							topics.append(line[i])
						mod = module.Module(name=line[0], topics=topics)
						moduleList.append(mod)

		#returns a list of tutor and module objects
		return [tutorList, moduleList]

	#This will convert a list of tutor and module objects into a text file, so that it can be used later
	def writeRequirements(self,tutorList, moduleList, filename):
		#Each tutor object and module object are converted into a string of comma separated values
		for tut in tutorList:
			tutorString = str(tut.name)

			for ex in tut.expertise:
				tutorString = tutorString + "," + str(ex)

			with open(filename, "a") as f:
				f.write(tutorString + "\n")

		with open(filename, "a") as f:
			f.write("===\n")

		for mod in moduleList:
			moduleString = str(mod.name)

			for top in mod.topics:
				moduleString = moduleString + "," + str(top)

			with open(filename, "a") as f:
				f.write(moduleString + "\n")

