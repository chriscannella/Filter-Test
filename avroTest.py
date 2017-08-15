from avro.datafile import DataFileReader
from avro.io import DatumReader

reader = DataFileReader(open("test_Ia_hsiao.avro", "rb"), DatumReader())

import filterinterp
# Make a calculator object and use it
inputFile = open('testFilter.txt', 'r')
filterProgram = inputFile.read()
inputFile.close()
calc = filterinterp.FilterInterpreter()
calc.initializeFilterProgram(filterProgram)

accepts = []
rejects = []
for alert in reader:
    calc.setCurrentObservation(alert)
    if alert['prv_candidates']:
        print alert['alertId'], alert['candidate']['jd'], alert['prv_candidates'][0]['jd'], alert['prv_candidates'][-1]['jd']
    if calc.interpret():
        accepts.append(alert['alertId'])
    else:
        rejects.append(alert['alertId'])
print [key for key in alert]
resultsFile = open("filterResults.txt", "w")
resultsFile.write("Accepted:\n")
for candid in accepts:
    resultsFile.write(str(candid) + '\n')
resultsFile.write("Rejected:\n")
for candid in rejects:
    resultsFile.write(str(candid) + '\n')
resultsFile.close()
