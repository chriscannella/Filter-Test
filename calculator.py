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
    import ply.lex as lex
    import ply.yacc as yacc

    # ------- Internal calculator state

    variables = {}       # Dictionary of stored variables

    # ------- Calculator tokenizing rules

    tokens = [
        'NAME', 'NUMBER', 'STRING', 
    ]

    reserved = {
        'in' : 'IN',
        'observation' : 'OBSERVATION'
    }

    tokens += reserved.values()

    literals = ['=', '+', '-', '*', '/', '(', ')', '[', ']']

    t_ignore = " \t"



    def t_NAME(t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if t.value in reserved:
            t.type = reserved[t.value]
        return t


    def t_STRING(t):
        r'\".*?\"'
        t.value = t.value[1:-1]
        return t

    def t_NUMBER(t):
        r'\d+\.?\d*'
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    lexer = lex.lex()

    # ------- Calculator parsing rules

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def p_statement_assign(p):
        'statement : NAME "=" expression'
        variables[p[1]] = p[3]
        p[0] = None

    def p_statement_expr(p):
        'statement : expression'
        p[0] = p[1]

    def p_expression_binop(p):
        '''expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression IN expression'''
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == 'in':
            p[0] = p[1] in p[3]

    def p_expression_uminus(p):
        "expression : '-' expression %prec UMINUS"
        p[0] = -p[2]

    def p_expression_group(p):
        "expression : '(' expression ')'"
        p[0] = p[2]

    def p_expression_field(p):
        "expression : expression '[' expression ']'"
        p[0] = p[1][p[3]]

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

    def p_error(p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    # Build the parser
    parser = yacc.yacc()

    # ------- Input function

    def input(text):
        result = parser.parse(text, lexer=lexer)
        return result

    return input

# Make a calculator object and use it
calc = make_calculator({'details' : {'mag' : 3}})

while True:
    try:
        s = raw_input("calc > ")
    except EOFError:
        break
    r = calc(s)
    if r:
        print(r)
