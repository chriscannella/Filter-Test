import filterlex
import filterparse_simul
import math

class FilterInterpreter():
    def __init__(self):
        self.current_observation = {}
        self.parser = filterparse_simul.FilterParser()

    def initializeFilterProgram(self, filterText):
        self.parser.initializeFilterProgram(filterText)

    def setCurrentObservation(self, current_observation):
        self.parser.setCurrentObservation(current_observation)

    def interpret(self):
        return self.parser.interpret()


