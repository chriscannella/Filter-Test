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
        self.filterProgram = ""
        self.syntaxtree = None
        self.tokens = filterlex.tokens
        self.lexer = filterlex
        self.build()
        self.current_observation = {}

    def initializeFilterProgram(self, filterText):
        unquoted = filterText.split('"')[::2]
        quoted = filterText.split('"')[1::2]
        formattedText = unquoted + quoted
        formattedText[::2] = [substring.lower() for substring in unquoted]
        formattedText[1::2] = quoted
        self.filterProgram = '"'.join(formattedText)
        self.syntaxtree = self.parser.parse(self.filterProgram, lexer=filterlex.lexer)

    def interpret(self):
        return self.syntaxtree[0](self.syntaxtree[1])

    def setCurrentObservation(self, current_observation):
        self.current_observation = current_observation

    def build(self):
        self.parser = yacc.yacc(module=self)

    def indent(self, x):
        return '\n'.join(['    ' + line for line in x.split('\n')])

    def compile(self):
        execText = "def compiledFunction(current_observation):\n"
        execText += self.indent("filteron = False\n" + self.syntaxtree + "return filteron\n")
        execText += "\nself.compiledFunction = compiledFunction\n"
        return execText

    def p_statementlist_statementblock(self, p):
        '''statementlist : statementlist statementblock
                         | statementblock '''
        if(len(p) > 2):
            p[0] = ("%s%s" %  (p[1], p[2]))
        else:
            p[0] = ("%s" % p[1])
    
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
                p[0] = ("while (%s):\n%s" % (p[3], self.indent(p[6])))
            elif p[1] == 'if':
                if len(p) > 8:
                    p[0] = ("if (%s):\n%selse:\n%s" % (p[3], self.indent(p[6]), self.indent(p[10])))
                else:
                    p[0] = ("if (%s):\n%s" % (p[3], self.indent(p[6])))
            elif p[1] == 'for':
                if len(p) > 8:
                    p[0] = ("%s\nwhile (%s):\n%s\n%s\n" % (p[3], p[5], self.indent(p[10]), self.indent(p[7])))
                else:
                    p[0] = ("for %s in %s:\n%s" % (p[2], p[4], self.indent(p[6])))
        elif(len(p) > 3):
            p[0] = ("%s" % p[2])
        else:
            p[0] = ("%s" % p[1])
    
    def p_statement_filteron(self, p):
        'statement : FILTERON expression'
        p[0] = ("filteron = %s\n" % p[2])
    
    def p_statement_expr(self, p):
        'statement : expression'
        p[0] = ("%s\n" % p[1])
    
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
        p[0] = ("%s %s %s" % (p[1], p[2], p[3]))
 
    
    def p_expression_uminus(self, p):
        "expression : MINUS expression %prec UMINUS"
        p[0] = ("(-%s)" % p[2])
    
    def p_expression_not(self, p):
        "expression : NOT expression"
        p[0] = ("(not %s)" % p[2])
    
    def p_expression_group(self, p):
        "expression : '(' expression ')'"
        p[0] = ("(%s)" % p[2])
    
    def p_expression_field(self, p):
        "expression : expression '[' expression ']'"
        p[0] = ("%s[%s]" % (p[1], p[3]))
    
    def p_expression_bool(self, p):
        '''expression : BOOL'''
        p[0] = ("%s" % (p[1] == 'true'))
    
    def p_expression_number(self, p):
        "expression : NUMBER"
        p[0] = ("%s" % p[1])
    
    def p_expression_string(self, p):
        "expression : STRING"
        p[0] = ("'%s'" % p[1])
    
    def p_expression_observation(self, p):
        "expression : OBSERVATION"
        p[0] = ("current_observation")
    
    def p_expression_function(self, p):
        "expression : NAME '(' expression ')'"
        namespace = ""
        if p[1] != 'len':
            namespace = "math."
        p[0] = ("%s(%s)" % (namespace + p[1], p[3]))
    
    def p_expression_assign(self, p):
        '''expression : NAME ASSIGN expression'''
        p[0] = ("%s = %s" % (p[1], p[3]))
    
    def p_expression_opassign(self, p):
        '''expression : NAME PLUSEQ expression
                      | NAME MINEQ expression
                      | NAME MULEQ expression
                      | NAME DIVEQ expression'''
        p[0] = ("%s %s %s" % (p[1], p[2], p[3]))
    
    
    def p_expression_name(self, p):
        "expression : NAME"
        p[0] = ("%s" % p[1])
    
    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
    
