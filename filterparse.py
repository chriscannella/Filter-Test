import filterlex
import ply.yacc as yacc

tokens = filterlex.tokens
# ------- Calculator tokenizing rules
precedence = (
    ('left', '+', '-'),
    ('left', 'MULTIPLY', '/'),
    ('right', 'UMINUS'),
)

def p_statementlist_statementblock(p):
    '''statementlist : statementlist statementblock
                     | statementblock '''
    if(len(p) > 2):
        p[0] = ('STATEMENTLIST','GATHER', 'LIST',  p[1], p[2])
    else:
        p[0] = ('STATEMENTLIST', 'GATHER', 'LIST', p[1])

def p_statementblock_statement(p):
    '''statementblock : '{' statementlist '}'
                      | WHILE '(' expression ')' '{' statementblock '}'
                      | IF '(' expression ')' '{' statementblock '}'
                      | IF '(' expression ')' '{' statementblock '}' ELSE '{' statementblock '}'
                      | FOR '(' expression ';' expression ';' expression ')' '{' statementblock '}'
                      | FOR NAME IN expression '{' statementblock '}' 
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

def p_statement_filteron(p):
    'statement : FILTERON expression'
    p[0] = ('STATEMENT', 'DO', 'FILTERON', p[2])

def p_statement_expr(p):
    'statement : expression'
    p[0] = ('STATEMENT','DO', 'EVALUATE', p[1])

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression MULTIPLY expression
                  | expression '/' expression
                  | expression IN expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression GEQ expression
                  | expression LEQ expression
                  | expression SG expression
                  | expression SL expression
                  | expression POWER expression'''
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

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = ('EXPRESSION', 'UNOP', 'UMINUS', p[2])

def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = ('EXPRESSION', 'MODIFY', 'PARENS', p[2])

def p_expression_field(p):
    "expression : expression '[' expression ']'"
    p[0] = ('EXPRESSION', 'MODIFY', 'FIELD', p[1], p[3])

def p_expression_bool(p):
    '''expression : BOOL'''
    p[0] = ('EXPRESSION', 'CONSTANT', 'BOOL', p[1])

def p_expression_number(p):
    "expression : NUMBER"
    p[0] = ('EXPRESSION', 'CONSTANT', 'NUMBER', p[1])

def p_expression_string(p):
    "expression : STRING"
    p[0] = ('EXPRESSION', 'CONSTANT', 'STRING', p[1])

def p_expression_observation(p):
    "expression : OBSERVATION"
    p[0] = ('EXPRESSION', 'GLOBAL', 'OBSERVATION')

def p_expression_assign(p):
    '''expression : NAME ASSIGN expression'''
    p[0] = ('EXPRESSION', 'LOCAL', 'ASSIGN', p[1], p[3])


def p_expression_name(p):
    "expression : NAME"
    p[0] = ('EXPRESSION', 'LOCAL', 'NAME', p[1])

def p_expression_test(p):
    "expression : TEST"
    p[0] = ('EXPRESSION', 'TEST', 'TEST')

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()
