import ply.lex as lex

# ------- Calculator tokenizing rules

tokens = [
    'NAME', 'NUMBER', 'STRING', 'ASSIGN', 'EQ', 'NEQ', 'GEQ', 'LEQ', 'SG', 'SL', 'BOOL'
]

reserved = {
    'in' : 'IN',
    'observation' : 'OBSERVATION',
    'filteron' : 'FILTERON',
    'test' : 'TEST',
    'while' : 'WHILE',
    'for' : 'FOR',
    'if' : 'IF',
    'else': 'ELSE'
}

tokens += reserved.values()

literals = ['+', '-', '*', '/', '(', ')', '[', ']','{', '}', ';', ':']

t_EQ = "=="
t_NEQ = "!="
t_GEQ = ">="
t_LEQ = "<="
t_SG = ">"
t_SL = "<"
t_ASSIGN = r"="
t_ignore = " \t"
t_BOOL = r"true|false"



def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in ['true', 'false']:
        t.type = 'BOOL'
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

lexer = lex.lex()
