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
    import ply.yacc as yacc

    # ------- Internal calculator state

    variables = {'filteron' : False}       # Dictionary of stored variables

    tokens = filterlex.tokens
    # ------- Calculator tokenizing rules
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def p_statementlist_statement(p):
        '''statementlist : statementlist ';' statement
                         | statement'''
        if(len(p) > 2):
            p[0] = p[3]
        else:
            p[0] = p[1]

    def p_statement_assign(p):
        '''statement : NAME ASSIGN expression'''
        variables[p[1]] = p[3]
        p[0] = None

    def p_statement_filteron(p):
        'statement : FILTERON expression'
        variables['filteron'] = p[2]
        p[0] = None

    def p_statement_expr(p):
        'statement : expression'
        p[0] = p[1]

    def p_expression_binop(p):
        '''expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression IN expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression GEQ expression
                      | expression LEQ expression
                      | expression SG expression
                      | expression SL expression'''
        if p[2] == '+':
            p[0] =  p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == 'in':
            p[0] = p[1] in p[3]
        elif p[2] == '==':
            p[0] = p[1] == p[3]
        elif p[2] == '!=':
            p[0] = p[1] != p[3]
        elif p[2] == '>=':
            p[0] = p[1] >= p[3]
        elif p[2] == '<=':
            p[0] = p[1] <= p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '<':
            p[0] = p[1] < p[3]

    def p_expression_uminus(p):
        "expression : '-' expression %prec UMINUS"
        p[0] = -p[2]

    def p_expression_group(p):
        "expression : '(' expression ')'"
        p[0] = p[2]

    def p_expression_field(p):
        "expression : expression '[' expression ']'"
        p[0] = p[1][p[3]]

    def p_expression_bool(p):
        '''expression : BOOL'''
        p[0] = p[1] == 'true'

    def p_expression_number(p):
        "expression : NUMBER"
        p[0] = p[1]

    def p_expression_string(p):
        "expression : STRING"
        p[0] = p[1]

    def p_expression_observation(p):
        "expression : OBSERVATION"
        p[0] = current_observation

    def p_expression_name(p):
        "expression : NAME"
        try:
            p[0] = variables[p[1]]
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

    def p_expression_test(p):
        "expression : TEST"
        if variables['filteron']:
            p[0] = True
        else:
            p[0] = False

    def p_error(p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    # Build the parser
    parser = yacc.yacc()

    # ------- Input function

    def input(text):
        result = parser.parse(text, lexer=filterlex.lexer)
        return result

    return input

# Make a calculator object and use it
testDict = {'details' : {'mag' : 3}}
calc = make_calculator(testDict)
testDict['details']['mag'] = 4
while True:
    try:
        s = raw_input("calc > ")
    except EOFError:
        break
    r = calc(s.lower())
    if r:
        print(r)
