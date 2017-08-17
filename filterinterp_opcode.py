import filterlex
import filterparse_opcode
import math

class FilterInterpreter():
    def __init__(self):
        self.initializeVariables()
        self.initializeFunctions()
        self.filterProgram = ""
        self.syntaxtree = None
        self.current_observation = {}

    def initializeVariables(self):
        self.variables = {'filteron' : False}

    def initializeFunctions(self):
        self.functions = {'sin' : math.sin, 'cos' : math.cos, 'tan' : math.tan, 'ceil' : math.ceil, 'abs' : math.fabs, 'factorial' : math.factorial, 'floor' : math.floor, 'isinf' : math.isinf, 'isnan' : math.isnan, 'exp' : math.exp, 'log' : math.log, 'log10' : math.log10, 'sqrt' : math.sqrt, 'acos' : math.acos, 'asin' : math.asin, 'atan' : math.atan, 'degrees' : math.degrees, 'radians' : math.radians, 'cosh' : math.cosh, 'sinh' : math.sinh, 'tanh' : math.tanh, 'acosh' : math.acosh, 'asinh' : math.asinh, 'atanh' : math.atanh, 'len' : len}

    def initializeFilterProgram(self, filterText):
        unquoted = filterText.split('"')[::2]
        quoted = filterText.split('"')[1::2]
        formattedText = unquoted + quoted
        formattedText[::2] = [substring.lower() for substring in unquoted]
        formattedText[1::2] = quoted
        self.filterProgram = '"'.join(formattedText)
        self.syntaxtree = filterparse.parser.parse(self.filterProgram, lexer=filterlex.lexer)

    def setCurrentObservation(self, current_observation):
        self.current_observation = current_observation

    def nodeTyper(self, nodeType, nodeActionType, nodeAction):
        if nodeType == 'STATEMENTLIST':
            return self.statementListActions(nodeActionType, nodeAction)
        if nodeType == 'STATEMENTBLOCK':
            return self.statementBlockActions(nodeActionType, nodeAction)
        elif nodeType == 'STATEMENT':
            return self.statementActions(nodeActionType, nodeAction)
        elif nodeType == 'EXPRESSION':
            return self.expressionActions(nodeActionType, nodeAction)
        else:
            return lambda x: 'NODE TYPE ERROR'

    def statementListActions(self, nodeActionType, nodeAction):
        if nodeActionType == 'GATHER':
            return self.statementListGather(nodeAction)
        else:
            return lambda x: 'STATEMENT LIST ERROR'

    def statementBlockActions(self, nodeActionType, nodeAction):
        if nodeActionType == 'GATHER':
            return self.statementBlockGather(nodeAction)
        if nodeActionType == 'CONTROL':
            return self.statementBlockControl(nodeAction)
        else:
            return lambda x: 'STATEMENT BLOCK ERROR'

    def statementActions(self, nodeActionType, nodeAction):
        if nodeActionType == 'DO':
            return self.statementDo(nodeAction)
        else:
            return lambda x: 'STATEMENT ACTION ERROR'

    def expressionActions(self, nodeActionType, nodeAction):
        if nodeActionType == 'BINOP':
            return self.expressionBinops(nodeAction)
        elif nodeActionType == 'CONSTANT':
            return self.expressionConstants(nodeAction)
        elif nodeActionType == 'UNOP':
            return self.expressionUnops(nodeAction)
        elif nodeActionType == 'MODIFY':
            return self.expressionModifications(nodeAction)
        elif nodeActionType == 'GLOBAL':
            return self.expressionGlobals(nodeAction)
        elif nodeActionType == 'LOCAL':
            return self.expressionLocals(nodeAction)
        else:
            return lambda x: 'EXPRESSION ACTION ERROR'

    def statementListGather(self, nodeAction):
        if nodeAction == 'LIST':
            return lambda x: ([self.evaluate(node) for node in x] and self.variables['filteron'])
        else:
            return lambda x: 'STATEMENTLIST ERROR'

    def statementBlockGather(self, nodeAction):
        if nodeAction == 'BRACKET':
            return lambda x: [self.evaluate(node) for node in x]
        else:
            return lambda x: 'STATEMENT BLOCK GATHER ERROR'

    def statementBlockControl(self, nodeAction):
        if nodeAction == 'WHILE':
            return self.whileFunction
        elif nodeAction == 'CFOR':
            return self.cforFunction
        elif nodeAction == 'PYFOR':
            pyforStep = lambda x : lambda nextVal : (variableAssignment(x[0], nextVal), self.evaluate(x[2]))
            return lambda x: map(pyforStep(x), self.evaluate(x[1]))
        elif nodeAction == 'IFTHEN':
            ifthenFunction = lambda x : (self.evaluate(x[0]) and self.evaluate(x[1]))
            return ifthenFunction
        elif nodeAction == 'IFTHENELSE':
            ifthenelseFunction = lambda x : (self.evaluate(x[0]) and self.evaluate(x[1])) or (self.evaluate(x[2]))
            return ifthenelseFunction
        else:
            return lambda x: 'STATEMENT BLOCK CONTROL ERROR'

    def whileFunction(self, x):
        while self.evaluate(x[0]):
            self.evaluate(x[1])
        return None

    def cforFunction(self, x):
        self.evaluate(x[0])
        while self.evaluate(x[1]):
            self.evaluate(x[2])
            self.evaluate(x[3])
        return None

    def statementDo(self, nodeAction):
        if nodeAction == 'EVALUATE':
            return lambda x: self.evaluate(x[0])
        elif nodeAction == 'FILTERON':
            return lambda x : self.variableAssignment('filteron', bool(self.evaluate(x[0])))
        else:
            return lambda x: 'STATEMENT DO ERROR'

    def expressionBinops(self, nodeAction):
        if nodeAction == 'ADD':
            return lambda x: self.evaluate(x[0]) + self.evaluate(x[1])
        elif nodeAction == 'SUBTRACT':
            return lambda x: self.evaluate(x[0]) - self.evaluate(x[1])
        elif nodeAction == 'MULTIPLY':
            return lambda x: self.evaluate(x[0]) * self.evaluate(x[1])
        elif nodeAction == 'DIVIDE':
            return lambda x: self.evaluate(x[0]) / self.evaluate(x[1])
        elif nodeAction == 'IN':
            return lambda x: self.evaluate(x[0]) in self.evaluate(x[1])
        elif nodeAction == 'EQ':
            return lambda x: self.evaluate(x[0]) == self.evaluate(x[1])
        elif nodeAction == 'NEQ':
            return lambda x: self.evaluate(x[0]) != self.evaluate(x[1])
        elif nodeAction == 'GEQ':
            return lambda x: self.evaluate(x[0]) >= self.evaluate(x[1])
        elif nodeAction == 'LEQ':
            return lambda x: self.evaluate(x[0]) <= self.evaluate(x[1])
        elif nodeAction == 'SG':
            return lambda x: self.evaluate(x[0]) > self.evaluate(x[1])
        elif nodeAction == 'SL':
            return lambda x: self.evaluate(x[0]) < self.evaluate(x[1])
        elif nodeAction == 'POWER':
            return lambda x: self.evaluate(x[0]) ** self.evaluate(x[1])
        elif nodeAction == 'AND':
            return lambda x: self.evaluate(x[0]) and self.evaluate(x[1])
        elif nodeAction == 'OR':
            return lambda x: self.evaluate(x[0]) or self.evaluate(x[1])
        else:
            return lambda x: 'EXPRESSION BINOP ERROR'

    def expressionUnops(self, nodeAction):
        if nodeAction == 'UMINUS':
            return lambda x : - self.evaluate(x[0])
        elif nodeAction == 'NOT':
            return lambda x : not self.evaluate(x[0])
        else:
            return lambda x : 'EXPRESSION UNOP ERROR'

    def expressionModifications(self, nodeAction):
        if nodeAction == 'PARENS':
            return lambda x : self.evaluate(x[0])
        if nodeAction == 'FIELD':
            return lambda x : self.evaluate(x[0])[self.evaluate(x[1])]
        else:
            return lambda x : 'EXPRESSION MODIFIER ERROR'

    def expressionGlobals(self, nodeAction):
        if nodeAction == 'OBSERVATION':
            return lambda x : self.current_observation
        elif nodeAction == 'FUNCTION':
            return lambda x : self.functions[x[0]](self.evaluate(x[1]))
        else:
            return lambda x : 'EXPRESSION GLOBALS ERROR'

    def expressionLocals(self, nodeAction):
        if nodeAction == 'NAME':
            return lambda x : self.retrieveVariable(x[0])
        elif nodeAction == 'ASSIGN':
            return lambda x: self.variableAssignment(x[0], self.evaluate(x[1]))
        elif nodeAction == 'PLUSEQ':
            return lambda x: self.variableAssignment(x[0], self.retrieveVariable(x[0]) + self.evaluate(x[1]))
        elif nodeAction == 'MINEQ':
            return lambda x: self.variableAssignment(x[0], self.retrieveVariable(x[0]) - self.evaluate(x[1]))
        elif nodeAction == 'MULEQ':
            return lambda x: self.variableAssignment(x[0], self.retrieveVariable(x[0]) * self.evaluate(x[1]))
        elif nodeAction == 'DIVEQ':
            return lambda x: self.variableAssignment(x[0], self.retrieveVariable(x[0]) / self.evaluate(x[1]))
        else:
            return lambda x : 'EXPRESSION LOCALS ERROR'

    def variableAssignment(self, variableName, variableValue):
        self.variables[variableName] = variableValue
        return True

    def retrieveVariable(self, variableName):
        variableValue = None
        try:
            variableValue = self.variables[variableName]
        except:
            variableValue = 'VARIABLE RETRIEVAL ERROR'
        return variableValue

    def expressionConstants(self, nodeAction):
        if nodeAction == 'NUMBER':
            return lambda x: x[0]
        elif nodeAction == 'STRING':
            return lambda x: x[0]
        elif nodeAction == 'BOOL':
            return lambda x: x[0] == 'true'
        else:
            return lambda x: 'EXPRESSION CONSTANT ERROR'

    def evaluate(self, node):
        nodeType = node[0]
        nodeActionType = node[1]
        nodeAction = node[2]
        nodeArguments = node[3:]
        return self.nodeTyper(nodeType, nodeActionType, nodeAction)(nodeArguments)

    def interpret(self):
        return self.evaluate(self.syntaxtree)


