# -----------------------------------------------------------------------------
# calc.py
#
# A calculator parser that makes use of closures. The function make_calculator()
# returns a function that accepts an input string and returns a result.  All
# lexing rules, parsing rules, and internal state are held inside the function.
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

# Make a calculator function



def make_calculator(current_observation=None):
    import filterlex
    import filterparse
    import math

    variables = {'filteron' : False}       # Dictionary of stored variables
    functions = {'sin' : math.sin, 'cos' : math.cos, 'tan' : math.tan, 'ceil' : math.ceil, 'abs' : math.fabs, 'factorial' : math.factorial, 'floor' : math.floor, 'isinf' : math.isinf, 'isnan' : math.isnan, 'exp' : math.exp, 'log' : math.log, 'log10' : math.log10, 'sqrt' : math.sqrt, 'acos' : math.acos, 'asin' : math.asin, 'atan' : math.atan, 'degrees' : math.degrees, 'radians' : math.radians, 'cosh' : math.cosh, 'sinh' : math.sinh, 'tanh' : math.tanh, 'acosh' : math.acosh, 'asinh' : math.asinh, 'atanh' : math.atanh}
    def nodeTyper(nodeType, nodeActionType, nodeAction):
        if nodeType == 'STATEMENTLIST':
            return statementListActions(nodeActionType, nodeAction)
        if nodeType == 'STATEMENTBLOCK':
            return statementBlockActions(nodeActionType, nodeAction)
        elif nodeType == 'STATEMENT':
            return statementActions(nodeActionType, nodeAction)
        elif nodeType == 'EXPRESSION':
            return expressionActions(nodeActionType, nodeAction)
        else:
            return lambda x: 'NODE TYPE ERROR'

    def statementListActions(nodeActionType, nodeAction):
        if nodeActionType == 'GATHER':
            return statementListGather(nodeAction)
        else:
            return lambda x: 'STATEMENT LIST ERROR'

    def statementBlockActions(nodeActionType, nodeAction):
        if nodeActionType == 'GATHER':
            return statementBlockGather(nodeAction)
        if nodeActionType == 'CONTROL':
            return statementBlockControl(nodeAction)
        else:
            return lambda x: 'STATEMENT BLOCK ERROR'

    def statementActions(nodeActionType, nodeAction):
        if nodeActionType == 'DO':
            return statementDo(nodeAction)
        else:
            return lambda x: 'STATEMENT ACTION ERROR'

    def expressionActions(nodeActionType, nodeAction):
        if nodeActionType == 'BINOP':
            return expressionBinops(nodeAction)
        elif nodeActionType == 'CONSTANT':
            return expressionConstants(nodeAction)
        elif nodeActionType == 'UNOP':
            return expressionUnops(nodeAction)
        elif nodeActionType == 'MODIFY':
            return expressionModifications(nodeAction)
        elif nodeActionType == 'GLOBAL':
            return expressionGlobals(nodeAction)
        elif nodeActionType == 'LOCAL':
            return expressionLocals(nodeAction)
        else:
            return lambda x: 'EXPRESSION ACTION ERROR'

    def statementListGather(nodeAction):
        if nodeAction == 'LIST':
            return lambda x: [evaluate(node) for node in x]
        else:
            return lambda x: 'STATEMENTLIST ERROR'

    def statementBlockGather(nodeAction):
        if nodeAction == 'BRACKET':
            return lambda x: [evaluate(node) for node in x]
        else:
            return lambda x: 'STATEMENT BLOCK GATHER ERROR'

    def statementBlockControl(nodeAction):
        if nodeAction == 'WHILE':
            return whileFunction
        elif nodeAction == 'CFOR':
            return cforFunction
        elif nodeAction == 'PYFOR':
            pyforStep = lambda x : lambda nextVal : (variableAssignment(x[0], nextVal), evaluate(x[2]))
            return lambda x: map(pyforStep(x), evaluate(x[1]))
        elif nodeAction == 'IFTHEN':
            ifthenFunction = lambda x : (evaluate(x[0]) and evaluate(x[1]))
            return ifthenFunction
        elif nodeAction == 'IFTHENELSE':
            ifthenelseFunction = lambda x : (evaluate(x[0]) and evaluate(x[1])) or (evaluate(x[2]))
            return ifthenelseFunction
        else:
            return lambda x: 'STATEMENT BLOCK CONTROL ERROR'

    def whileFunction(x):
        while evaluate(x[0]):
            evaluate(x[1])
        return None

    def cforFunction(x):
        evaluate(x[0])
        while evaluate(x[1]):
            evaluate(x[2])
            evaluate(x[3])
        return None

    def statementDo(nodeAction):
        if nodeAction == 'EVALUATE':
            return lambda x: evaluate(x[0])
        elif nodeAction == 'FILTERON':
            return lambda x : variables['filteron']
        else:
            return lambda x: 'STATEMENT DO ERROR'



    def expressionBinops(nodeAction):
        if nodeAction == 'ADD':
            return lambda x: evaluate(x[0]) + evaluate(x[1])
        elif nodeAction == 'SUBTRACT':
            return lambda x: evaluate(x[0]) - evaluate(x[1])
        elif nodeAction == 'MULTIPLY':
            return lambda x: evaluate(x[0]) * evaluate(x[1])
        elif nodeAction == 'DIVIDE':
            return lambda x: evaluate(x[0]) / evaluate(x[1])
        elif nodeAction == 'IN':
            return lambda x: evaluate(x[0]) in evaluate(x[1])
        elif nodeAction == 'EQ':
            return lambda x: evaluate(x[0]) == evaluate(x[1])
        elif nodeAction == 'NEQ':
            return lambda x: evaluate(x[0]) != evaluate(x[1])
        elif nodeAction == 'GEQ':
            return lambda x: evaluate(x[0]) >= evaluate(x[1])
        elif nodeAction == 'LEQ':
            return lambda x: evaluate(x[0]) <= evaluate(x[1])
        elif nodeAction == 'SG':
            return lambda x: evaluate(x[0]) > evaluate(x[1])
        elif nodeAction == 'SL':
            return lambda x: evaluate(x[0]) < evaluate(x[1])
        elif nodeAction == 'POWER':
            return lambda x: evaluate(x[0]) ** evaluate(x[1])
        else:
            return lambda x: 'EXPRESSION BINOP ERROR'

    def expressionUnops(nodeAction):
        if nodeAction == 'UMINUS':
            return lambda x : - evaluate(x[0])
        else:
            return lambda x : 'EXPRESSION UNOP ERROR'

    def expressionModifications(nodeAction):
        if nodeAction == 'PARENS':
            return lambda x : evaluate(x[0])
        if nodeAction == 'FIELD':
            return lambda x : evaluate(x[0])[evaluate(x[1])]
        else:
            return lambda x : 'EXPRESSION MODIFIER ERROR'

    def expressionGlobals(nodeAction):
        if nodeAction == 'OBSERVATION':
            return lambda x : current_observation
        elif nodeAction == 'FUNCTION':
            return lambda x : functions[x[0]](evaluate(x[1]))
        else:
            return lambda x : 'EXPRESSION GLOBALS ERROR'

    def expressionLocals(nodeAction):
        if nodeAction == 'NAME':
            return lambda x : retrieveVariable(x[0])
        elif nodeAction == 'ASSIGN':
            return lambda x: variableAssignment(x[0], evaluate(x[1]))
        elif nodeAction == 'PLUSEQ':
            return lambda x: variableAssignment(x[0], retrieveVariable(x[0]) + evaluate(x[1]))
        elif nodeAction == 'MINEQ':
            return lambda x: variableAssignment(x[0], retrieveVariable(x[0]) - evaluate(x[1]))
        elif nodeAction == 'MULEQ':
            return lambda x: variableAssignment(x[0], retrieveVariable(x[0]) * evaluate(x[1]))
        elif nodeAction == 'DIVEQ':
            return lambda x: variableAssignment(x[0], retrieveVariable(x[0]) / evaluate(x[1]))
        else:
            return lambda x : 'EXPRESSION LOCALS ERROR'

    def variableAssignment(variableName, variableValue):
        variables[variableName] = variableValue
        return True

    def retrieveVariable(variableName):
        variableValue = None
        try:
            variableValue = variables[variableName]
        except:
            variableValue = 'VARIABLE RETRIEVAL ERROR'
        return variableValue

    def expressionConstants(nodeAction):
        if nodeAction == 'NUMBER':
            return lambda x: x[0]
        elif nodeAction == 'STRING':
            return lambda x: x[0]
        elif nodeAction == 'BOOL':
            return lambda x: x[0] == 'true'
        else:
            return lambda x: 'EXPRESSION CONSTANT ERROR'

    def evaluate(node):
        nodeType = node[0]
        nodeActionType = node[1]
        nodeAction = node[2]
        nodeArguments = node[3:]
        return nodeTyper(nodeType, nodeActionType, nodeAction)(nodeArguments)

    def interpret(text):
        syntaxtree = filterparse.parser.parse(text, lexer=filterlex.lexer)
        return evaluate(syntaxtree)

    return interpret

# Make a calculator object and use it
testDict = {'details' : {'mag' : 3}, 'list' : [1, 2, 3, 4, 55]}
calc = make_calculator(testDict)
testDict['details']['mag'] = 4
inputFile = open('testFilter.txt', 'r')
r = calc(inputFile.read().lower())
if r:
    print(r)
inputFile.close()
