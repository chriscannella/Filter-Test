from avro.datafile import DataFileReader
from avro.io import DatumReader
import random
import timeit
reader = DataFileReader(open("test_Ia_hsiao.avro", "rb"), DatumReader())

def testRandomAlert(calc, alertList):
    calc.setCurrentObservation(random.choice(alertList))
    return calc.interpret()

import filterinterp_opcode
import filterinterp_simul
import filterinterp_compiled
import filterinterp_python

# Make a calculator object and use it
inputFile = open('testFilter.txt', 'r')
filterProgram = inputFile.read()
inputFile.close()

alertList = []
for alert in reader:
    alertList.append(alert)

numexec = 100000
calc = filterinterp_opcode.FilterInterpreter()
calc.initializeFilterProgram(filterProgram)
totalTime = timeit.timeit("testRandomAlert(calc, alertList)", setup='from __main__ import testRandomAlert, calc, alertList', number=numexec)
print "Opcode based Filter Language Interpreter:"
print "Total time:", totalTime
print "Average decision time: ", totalTime/numexec


calc = filterinterp_simul.FilterInterpreter()
calc.initializeFilterProgram(filterProgram)
totalTime = timeit.timeit("testRandomAlert(calc, alertList)", setup='from __main__ import testRandomAlert, calc, alertList', number=numexec)
print "Simultaneous Parse/Execute Filter Language Interpreter:"
print "Total time:", totalTime
print "Average decision time: ", totalTime/numexec

calc = filterinterp_compiled.FilterInterpreter()
calc.initializeFilterProgram(filterProgram)
totalTime = timeit.timeit("testRandomAlert(calc, alertList)", setup='from __main__ import testRandomAlert, calc, alertList', number=numexec)
print "Python Compiled Filter Language Interpreter:"
print "Total time:", totalTime
print "Average decision time: ", totalTime/numexec

calc = filterinterp_python.FilterInterpreter()
calc.initializeFilterProgram(filterProgram)
totalTime = timeit.timeit("testRandomAlert(calc, alertList)", setup='from __main__ import testRandomAlert, calc, alertList', number=numexec)
print "Raw Python Filter:"
print "Total time:", totalTime
print "Average decision time: ", totalTime/numexec

