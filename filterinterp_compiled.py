import filterlex
import filterparse_compiled
import math

class FilterInterpreter():
    def __init__(self):
        self.current_observation = {}
        self.functionText = ""
        self.parser = filterparse_compiled.FilterParser()

    def initializeFilterProgram(self, filterText):
        self.parser.initializeFilterProgram(filterText)
        self.functionText = self.parser.compile()
        exec(self.functionText)

    def setCurrentObservation(self, current_observation):
        self.current_observation = current_observation

    def interpret(self):
        return self.compiledFunction(self.current_observation)

