import math
import filterlex
import ply.yacc as yacc

class FilterParser():
    # ------- Calculator tokenizing rules
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE'),
        ('right', 'UMINUS'),
    )
    def __init__(self):
        self.initializeVariables()
        self.initializeFunctions()
        self.filterProgram = ""
        self.syntaxtree = None
        self.tokens = filterlex.tokens
        self.lexer = filterlex
        self.build()
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
        self.initializeVariables()
        self.initializeFunctions()
        self.syntaxtree = self.parser.parse(self.filterProgram, lexer=filterlex.lexer)

    def interpret(self):
        return self.syntaxtree[0](self.syntaxtree[1])

    def setCurrentObservation(self, current_observation):
        self.current_observation = current_observation

    def build(self):
        self.parser = yacc.yacc(module=self)

    def p_statementlist_statementblock(self, p):
        '''statementlist : statementlist statementblock
                         | statementblock '''
        if(len(p) > 2):
            p[0] = (lambda x: ([node[0](node[1]) for node in x] and self.variables['filteron']),  (p[1], p[2]))
        else:
            p[0] = (lambda x: (x[0](x[1]) and self.variables['filteron']), (p[1]))
    
    def whileFunction(self, x):
        while x[0][0](x[0][1]):
            x[1][0](x[1][1])
        return None

    def cforFunction(self, x):
        x[0][0](x[0][1])
        while x[1][0](x[1][1]):
            x[2][0](x[2][1])
            x[3][0](x[3][1])
        return None

    def pyforStep(self, x):
        return lambda nextVal : (variableAssignment(x[0], nextVal), x[2][0](x[2][1]))

    def p_statementblock_statement(self, p):
        '''statementblock : '{' statementlist '}'
                          | WHILE '(' expression ')' '{' statementlist '}'
                          | IF '(' expression ')' '{' statementlist '}'
                          | IF '(' expression ')' '{' statementlist '}' ELSE '{' statementlist '}'
                          | FOR '(' expression ';' expression ';' expression ')' '{' statementlist '}'
                          | FOR NAME IN expression '{' statementlist '}' 
                          | statement ';' '''
        if(len(p) > 4):
            if p[1] == 'while':
                p[0] = (self.whileFunction, (p[3], p[6]))
            elif p[1] == 'if':
                if len(p) > 8:
                    p[0] = (lambda x : (x[0][0](x[0][1]) and x[1][0](x[1][1])) or (x[2][0](x[2])), (p[3], p[6], p[10]))
                else:
                    p[0] = (lambda x : (x[0][0](x[0][1]) and x[1][0](x[1][1])), (p[3], p[6]))
            elif p[1] == 'for':
                if len(p) > 8:
                    p[0] = (self.cforFunction, (p[3], p[5], p[7], p[10]))
                else:
                    p[0] = (lambda x: map(pyforStep(x), x[1][0](x[1][1])), (p[2], p[4], p[6]))
        elif(len(p) > 3):
            p[0] = (lambda x: x[0](x[1]), (p[2]))
        else:
            p[0] = (lambda x: x[0](x[1]), (p[1]))
    
    def p_statement_filteron(self, p):
        'statement : FILTERON expression'
        p[0] = (lambda x : self.variableAssignment('filteron', bool(x[0](x[1]))), (p[2]))
    
    def p_statement_expr(self, p):
        'statement : expression'
        p[0] = (lambda x: x[0](x[1]), (p[1]))
    
    def p_expression_binop(self, p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression MULTIPLY expression
                      | expression DIVIDE expression
                      | expression IN expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression GEQ expression
                      | expression LEQ expression
                      | expression SG expression
                      | expression SL expression
                      | expression POWER expression
                      | expression AND expression
                      | expression OR expression'''
        if p[2] == '+':
            p[0] =  (lambda x: x[0][0](x[0][1]) + x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == '-':
            p[0] =  (lambda x: x[0][0](x[0][1]) - x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == '*':
            p[0] =  (lambda x: x[0][0](x[0][1]) * x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == '/':
            p[0] =  (lambda x: x[0][0](x[0][1]) / x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == 'in':
            p[0] =  (lambda x: x[0][0](x[0][1]) in x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == '==':
            p[0] =  (lambda x: x[0][0](x[0][1]) == x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == '!=':
            p[0] =  (lambda x: x[0][0](x[0][1]) != x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == '>=':
            p[0] =  (lambda x: x[0][0](x[0][1]) >= x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == '<=':
            p[0] =  (lambda x: x[0][0](x[0][1]) <= x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == '>':
            p[0] =  (lambda x: x[0][0](x[0][1]) > x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == '<':
            p[0] =  (lambda x: x[0][0](x[0][1]) < x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == '**':
            p[0] =  (lambda x: x[0][0](x[0][1]) ** x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == 'and':
            p[0] =  (lambda x: x[0][0](x[0][1]) and x[1][0](x[1][1]), (p[1], p[3]))
        elif p[2] == 'or':
            p[0] =  (lambda x: x[0][0](x[0][1]) or x[1][0](x[1][1]), (p[1], p[3]))
    
    
    def p_expression_uminus(self, p):
        "expression : MINUS expression %prec UMINUS"
        p[0] = (lambda x : - x[0](x[1]), (p[2]))
    
    def p_expression_not(self, p):
        "expression : NOT expression"
        p[0] = (lambda x : not x[0](x[1]), (p[2]))
    
    def p_expression_group(self, p):
        "expression : '(' expression ')'"
        p[0] = (lambda x : x[0](x[1]), (p[2]))
    
    def p_expression_field(self, p):
        "expression : expression '[' expression ']'"
        p[0] = (lambda x : x[0][0](x[0][1])[x[1][0](x[1][1])], (p[1], p[3]))
    
    def p_expression_bool(self, p):
        '''expression : BOOL'''
        p[0] = (lambda x : x == 'true', (p[1]))
    
    def p_expression_number(self, p):
        "expression : NUMBER"
        p[0] = (lambda x: x, (p[1]))
    
    def p_expression_string(self, p):
        "expression : STRING"
        p[0] = (lambda x: x, (p[1]))
    
    def p_expression_observation(self, p):
        "expression : OBSERVATION"
        p[0] = (lambda x : self.current_observation, ())
    
    def p_expression_function(self, p):
        "expression : NAME '(' expression ')'"
        p[0] = (lambda x : self.functions[x[0]](x[1][0](x[1][1])), (p[1], p[3]))
    
    def variableAssignment(self, variableName, variableValue):
        self.variables[variableName] = variableValue
        return True

    def p_expression_assign(self, p):
        '''expression : NAME ASSIGN expression'''
        p[0] = (lambda x: self.variableAssignment(x[0], x[1][0](x[1][1])), (p[1], p[3]))
    
    def p_expression_opassign(self, p):
        '''expression : NAME PLUSEQ expression
                      | NAME MINEQ expression
                      | NAME MULEQ expression
                      | NAME DIVEQ expression'''
        if p[2] == '+=':
            p[0] = (lambda x: self.variableAssignment(x[0], self.variables[x[0]] + x[1][0](x[1][1])), (p[1], p[3]))
        if p[2] == '-=':
            p[0] = (lambda x: self.variableAssignment(x[0], self.variables[x[0]] - x[1][0](x[1][1])), (p[1], p[3]))
        if p[2] == '*=':
            p[0] = (lambda x: self.variableAssignment(x[0], self.variables[x[0]] * x[1][0](x[1][1])), (p[1], p[3]))
        if p[2] == '/=':
            p[0] = (lambda x: self.variableAssignment(x[0], self.variables[x[0]] / x[1][0](x[1][1])), (p[1], p[3]))
    
    
    def p_expression_name(self, p):
        "expression : NAME"
        p[0] = (lambda x: self.variables[x], (p[1]))
    
    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
    
