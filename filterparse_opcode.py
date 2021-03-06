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
        self.tokens = filterlex.tokens
        self.lexer = filterlex
        self.build()

    def build(self):
        self.parser = yacc.yacc(module=self)

    def p_statementlist_statementblock(self, p):
        '''statementlist : statementlist statementblock
                         | statementblock '''
        if(len(p) > 2):
            p[0] = ('STATEMENTLIST','GATHER', 'LIST',  p[1], p[2])
        else:
            p[0] = ('STATEMENTLIST', 'GATHER', 'LIST', p[1])
    
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
                p[0] = ('STATEMENTBLOCK', 'CONTROL', 'WHILE', p[3], p[6])
            elif p[1] == 'if':
                if len(p) > 8:
                    p[0] = ('STATEMENTBLOCK', 'CONTROL', 'IFTHENELSE', p[3], p[6], p[10])
                else:
                    p[0] = ('STATEMENTBLOCK', 'CONTROL', 'IFTHEN', p[3], p[6])
            elif p[1] == 'for':
                if len(p) > 8:
                    p[0] = ('STATEMENTBLOCK', 'CONTROL', 'CFOR', p[3], p[5], p[7], p[10])
                else:
                    p[0] = ('STATEMENTBLOCK', 'CONTROL', 'PYFOR', p[2], p[4], p[6])
        elif(len(p) > 3):
            p[0] = ('STATEMENTBLOCK', 'GATHER', 'BRACKET', p[2])
        else:
            p[0] = ('STATEMENTBLOCK', 'GATHER', 'BRACKET', p[1])
    
    def p_statement_filteron(self, p):
        'statement : FILTERON expression'
        p[0] = ('STATEMENT', 'DO', 'FILTERON', p[2])
    
    def p_statement_expr(self, p):
        'statement : expression'
        p[0] = ('STATEMENT','DO', 'EVALUATE', p[1])
    
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
            p[0] =  ('EXPRESSION', 'BINOP', 'ADD', p[1], p[3])
        elif p[2] == '-':
            p[0] = ('EXPRESSION', 'BINOP', 'SUBTRACT', p[1], p[3])
        elif p[2] == '*':
            p[0] = ('EXPRESSION', 'BINOP', 'MULTIPLY', p[1], p[3])
        elif p[2] == '/':
            p[0] = ('EXPRESSION', 'BINOP', 'DIVIDE', p[1], p[3])
        elif p[2] == 'in':
            p[0] = ('EXPRESSION', 'BINOP', 'IN', p[1], p[3])
        elif p[2] == '==':
            p[0] = ('EXPRESSION', 'BINOP', 'EQ', p[1], p[3])
        elif p[2] == '!=':
            p[0] = ('EXPRESSION', 'BINOP', 'NEQ', p[1], p[3])
        elif p[2] == '>=':
            p[0] = ('EXPRESSION', 'BINOP', 'GEQ', p[1], p[3])
        elif p[2] == '<=':
            p[0] = ('EXPRESSION', 'BINOP', 'LEQ', p[1], p[3])
        elif p[2] == '>':
            p[0] = ('EXPRESSION', 'BINOP', 'SG', p[1], p[3])
        elif p[2] == '<':
            p[0] = ('EXPRESSION', 'BINOP', 'SL', p[1], p[3])
        elif p[2] == '**':
            p[0] = ('EXPRESSION', 'BINOP', 'POWER', p[1], p[3])
        elif p[2] == 'and':
            p[0] = ('EXPRESSION', 'BINOP', 'AND', p[1], p[3])
        elif p[2] == 'or':
            p[0] = ('EXPRESSION', 'BINOP', 'OR', p[1], p[3])
    
    
    def p_expression_uminus(self, p):
        "expression : MINUS expression %prec UMINUS"
        p[0] = ('EXPRESSION', 'UNOP', 'UMINUS', p[2])
    
    def p_expression_not(self, p):
        "expression : NOT expression"
        p[0] = ('EXPRESSION', 'UNOP', 'NOT', p[2])
    
    def p_expression_group(self, p):
        "expression : '(' expression ')'"
        p[0] = ('EXPRESSION', 'MODIFY', 'PARENS', p[2])
    
    def p_expression_field(self, p):
        "expression : expression '[' expression ']'"
        p[0] = ('EXPRESSION', 'MODIFY', 'FIELD', p[1], p[3])
    
    def p_expression_bool(self, p):
        '''expression : BOOL'''
        p[0] = ('EXPRESSION', 'CONSTANT', 'BOOL', p[1])
    
    def p_expression_number(self, p):
        "expression : NUMBER"
        p[0] = ('EXPRESSION', 'CONSTANT', 'NUMBER', p[1])
    
    def p_expression_string(self, p):
        "expression : STRING"
        p[0] = ('EXPRESSION', 'CONSTANT', 'STRING', p[1])
    
    def p_expression_observation(self, p):
        "expression : OBSERVATION"
        p[0] = ('EXPRESSION', 'GLOBAL', 'OBSERVATION')
    
    def p_expression_function(self, p):
        "expression : NAME '(' expression ')'"
        p[0] = ('EXPRESSION', 'GLOBAL', 'FUNCTION', p[1], p[3])
    
    def p_expression_assign(self, p):
        '''expression : NAME ASSIGN expression'''
        p[0] = ('EXPRESSION', 'LOCAL', 'ASSIGN', p[1], p[3])
    
    def p_expression_opassign(self, p):
        '''expression : NAME PLUSEQ expression
                      | NAME MINEQ expression
                      | NAME MULEQ expression
                      | NAME DIVEQ expression'''
        if p[2] == '+=':
            p[0] = ('EXPRESSION', 'LOCAL', 'PLUSEQ', p[1], p[3])
        if p[2] == '-=':
            p[0] = ('EXPRESSION', 'LOCAL', 'MINEQ', p[1], p[3])
        if p[2] == '*=':
            p[0] = ('EXPRESSION', 'LOCAL', 'MULEQ', p[1], p[3])
        if p[2] == '/=':
            p[0] = ('EXPRESSION', 'LOCAL', 'DIVEQ', p[1], p[3])
    
    
    def p_expression_name(self, p):
        "expression : NAME"
        p[0] = ('EXPRESSION', 'LOCAL', 'NAME', p[1])
    
    def p_expression_test(self, p):
        "expression : TEST"
        p[0] = ('EXPRESSION', 'TEST', 'TEST')
    
    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
    
