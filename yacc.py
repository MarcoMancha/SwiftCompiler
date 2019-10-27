# Marco Antonio Mancha Alfaro A01206194
# Analizador lexico Swift

import ply.yacc as yacc
from lexer import MyLexer
import json

# Obtener tokens de lexer
m = MyLexer()
m.build()
tokens = m.tokens

# Simbolo inicial
def p_code_unit(p):
    """
    code-unit : statement-r
    """
    p[0] = (p[1])

# Simbolo auxiliar
def p_statement_r(p):
    """
    statement-r : statement statement-r
              | empty
    """
    try:
        p[0] = (p[1], (p[2]))
    except:
        p[0] = (p[1])

# Proyeccion base para generar codigo
def p_statement(p):
    """
    statement  :  SEMICOLON
               | block
               | if
               | var-decl
               | while
               | else
               | assignment
               | out
               | class-decl
               | func-decl
    """
    p[0] = (p[1])

def p_class_decl(p):
    """
    class-decl   :  CLASS id-class block
    """
    p[0] = ('CLASS',p[1],p[2])

def p_func_decl(p):
    """
    func-decl   :  STATIC FUNCTION id-function LPAREN RPAREN block
    """
    p[0] = ('FUNCTION',p[3],p[6])

def p_out(p):
    """
    out  : OUTPUT LPAREN expr RPAREN
    """
    p[0] = ('OUTPUT', p[3])
        

# Declaracion de variable
def p_var_decl(p):
    """
    var-decl  :  prefix rest-decl
    """
    p[0] = ('VAR_DECL',p[1], p[2])

# Parte postfija de declaracion de variable
def p_rest_decl(p):
    """
    rest-decl  :  id-decl suffix  assign-empty
    """
    p[0] = ('REST_DECL', p[1], p[2], p[3])

# Vacio
def p_empty(p):
    """
    empty :
    """
    p[0] = (None)

# Asignacion a valor o vacio
def p_assign_empty(p):
    """
    assign-empty : ASSIGN expr
	             | empty
    """
    try: 
        p[0] = (p[2])
    except:
        p[0] = None

# Asignacion de tipo (variable/constante)
def p_prefix(p):
    """
    prefix  :  D_VAR
            |  D_LET
    """
    p[0] = (p[1])

# Asignacion de clase (Int/Bool/String)
def p_suffix(p):
    """
    suffix  : COLON class
	| empty
    """
    try:
        p[0] = (p[2])
    except:
        p[0] = None

# Proyeccion a clases
def p_class(p):
    """
    class  :  class-literal
    """
    p[0] = (p[1])

# Expresion base para expresion 
def p_base_expr(p):
    """
    base-expr  :  literal
                | id empty
                | LPAREN expr RPAREN
                | input
                | class-name
                | func-inv
    """
    if len(p) == 4:
        p[0] = (p[2])
    elif len(p) == 3:
        temp_i = m.index
        while temp_i >= 0:
            try: 
                m.variables[temp_i][p[1]]
                break
            except:
                pass
            temp_i = temp_i - 1

        if temp_i < 0:
            print("\nUndeclared variable '%s'" % p[1])

        p[0] = (p[1])
    else:
        p[0] = (p[1])

# Input usuario
def p_input(p):
    """
    input : INPUT LPAREN RPAREN
    """
    p[0] = ('INPUT',p[1])

# Llamada clase
def p_class_name(p):
    """
    class-name : id LPAREN RPAREN
    """
    try: 
        m.classes[p[1]]
    except:
        print("\nUndefined class '%s'" % p[1])
    p[0] = ('CLASS',p[1])

# Llamada methodo
def p_func_name(p):
    """
    func-name : id LPAREN RPAREN
    """
    try: 
        m.functions[p[1]]
    except:
        print("\nUndefined method '%s'" % p[1])
    p[0] = ('FUNCTION',p[1])

# Llamada funcion clase
def p_func_inv(p):
    """
    func-inv    :   id DOT func-name
    """
    temp_i = m.index
    while temp_i >= 0:
        try: 
            m.variables[temp_i][p[1]]
            break
        except:
            pass
        temp_i = temp_i - 1

    if temp_i < 0:
        print("\nUndeclared variable '%s'" % p[1])

    p[0] = (p[1])

# Definicion variable
def p_id(p):
    """
    id  :  ID
    """
    p[0] = (p[1])

# Definicion variable
def p_id_decl(p):
    """
    id-decl :  ID
    """
    m.variables[m.index][p[1]] = 1
    p[0] = (p[1])

# Definicion clase
def p_id_class(p):
    """
    id-class :  id
    """
    m.classes[p[1]] = []
    p[0] = (p[1])

# Definicion funcion
def p_id_function(p):
    """
    id-function :  id
    """
    m.functions[p[1]] = 1
    p[0] = (p[1])

# Tipos de datos
def p_literal(p):
    """
    literal  :  STR_LITERAL
            | INT
            | bool
    """
    p[0] = (p[1])

# Clases posibles para tipo de dato
def p_class_literal(p):
    """
    class-literal  :  class_String
                   |  class_BOOL
                   |  class_CHARACTER
                   |  class_INT
    """
    p[0] = (p[1])

# Proyeccion valores boolean
def p_bool(p):
    """
    bool  :  E_TRUE
          | E_FALSE
    """
    p[0] = (p[1])

# Proyeccion para expresion logica
def p_expr(p):
    """
    expr  :  or-expr
    """
    p[0] = (p[1])

# Proyeccion para construccion usando operador logico ||
def p_or_expr(p):
    """
    or-expr  :  and-expr
            | or-expr LOG_OR and-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = (p[1])

# Proyeccion para construccion usando operador logico &&
def p_and_expr(p):
    """
    and-expr  :  eq-expr
             | and-expr LOG_AND eq-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = (p[1])

# Proyeccion para construccion usando operador logico == o !=
def p_eq_expr(p):
    """
    eq-expr  :  cmp-expr
            | eq-expr eq-or-not-eq eq-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = (p[1])

# Definicion de opciones comparacion
def p_eq_or_not_eq(p):
    """
    eq-or-not-eq    : EQUAL
                   | NOT_EQUAL
    """
    p[0] = (p[1])

# Proyeccion para poder usar gramatica comparacion < <= == > >=
def p_cmp_expr(p):
    """
    cmp-expr  :  add-expr
             | cmp-expr compare add-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = (p[1])

# Proyeccion simbolos terminales comparacion
def p_compare(p):
    """
    compare : LESS
             | LESS_EQ
             | EQUAL
             | GREATER
             | GREATER_EQ
    """
    p[0] = (p[1])

# Proyeccion inicial operacion matematica
def p_add_expr(p):
    """
    add-expr  :  mult-expr
             | add-expr plus-minus mult-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = (p[1])

# Proyeccion terminales para sumar y restar
def p_plus_minus(p):
    """
    plus-minus    : PLUS
                  | MINUS
    """
    p[0] = (p[1])

# Proyeccion para poder usar expresion unaria u operaciones * /
def p_mult_expr(p):
    """
    mult-expr  :  unary-expr
               | mult-expr mult-div unary-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = (p[1])

# Proyeccion terminales multiplicacion y division
def p_mult_div(p):
    """
    mult-div   : MULT
               | DIV
    """
    p[0] = (p[1])

# Proyeccion de operaciones unarias y posible operacion postfija
def p_unary_expr(p):
    """
    unary-expr  :  postfix-expr
                 | minus postfix-expr
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[1])


def p_minus(p):
    """
    minus   : MINUS
    """
    p[0] = (p[1])

# Proyeccion operacion postfija
def p_postfix_expr(p):
    """
    postfix-expr  :  base-expr
                 | postfix-expr base-expr
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[1])

# Proyeccion para estructura de codigo dentro de un bloque
def p_block(p):
    """
    block  :  LBRACE new-scope code-unit RBRACE
    """
    p[0] = ('BLOCK', (p[2]))
    m.index = m.index - 1
    m.variables = m.variables[:-1]

def p_new_scope(p):
    """
    new-scope :
    """
    m.variables.append({})
    m.index = m.index + 1

# Proyeccion de asignacion de valor
def p_assignment(p):
    """
    assignment  : assign expr
    """
    p[0] = ('ASSIGNMENT', p[1], p[2])

def p_assign(p):
    """
    assign    : ASSIGN
    """
    p[0] = (p[1])

# Proyeccion construccion sentencia if
def p_if(p):
    """
    if  :  S_IF LPAREN expr RPAREN block else
    """
    p[0] = ('IF', p[3], p[5], p[6])

# Proyeccion construccion sentencia else
def p_else(p):
    """
    else   : S_ELSE block
           | empty
    """
    try:
        p[0] = ('ELSE', p[2])
    except:
        p[0] = (p[1])

# Proyeccion construccion sentencia while
def p_while(p):
    """
    while  :    S_WHILE LPAREN expr RPAREN block
    """
    p[0] = ('WHILE', p[1], p[3], p[5])

# Manejo de errores
def p_error(p):
    if p:
        print("-------------------------------")
        print("Syntax error at token", p.type)
        print("Syntax error at '%s'" % p.value)
        print("line : '%s'" % p.lineno)
        print("-------------------------------")
        # parser.errok()
    else:
        print("Syntax error at EOF")

# Generar test y reiniciar variables globales lexer
def parse_test(test):
    m.variables = [{}]
    m.index = 0
    file = open(test)
    data = file.read()
    print("\n")
    print(data)
    ast = parser.parse(data)
    l = test.split('/')
    folder = l[0]
    name = l[1]
    file = open(folder+"/AST-"+name, 'w')
    file.write(json.dumps(ast, indent=2))

# Iniciar Pruebas

parser = yacc.yacc(debug=False)

# Pruebas 1era entrega 

# print("\n--------PRUEBA 1--------\n")       
# parse_test('pruebas/1.txt')
# print("\n")
# print("\n--------PRUEBA 2--------\n")       
# parse_test('pruebas/2.txt')
# print("\n")
# print("\n--------PRUEBA 3--------\n")       
# parse_test('pruebas/3.txt')
# print("\n")
# print("\n--------PRUEBA 4--------\n")       
# parse_test('pruebas/4.txt')
# print("\n")
# print("\n--------PRUEBA 5--------\n")       
# parse_test('pruebas/5.txt')
# print("\n")
# print("\n--------PRUEBA 6--------\n")       
# parse_test('pruebas/6.txt')
# print("\n")
# print("\n--------PRUEBA 7--------\n")       
# parse_test('pruebas/7.txt')
# print("\n")
# print("\n--------PRUEBA 8--------\n")       
# parse_test('pruebas/8.txt')
# print("\n")
# print("\n--------PRUEBA 9--------\n")       
# parse_test('pruebas/9.txt')
# print("\n")
# print("\n--------PRUEBA 10--------\n")       
# parse_test('pruebas/10.txt')
# print("\n")
# print("\n--------PRUEBA 11--------\n")       
# parse_test('pruebas/11.txt')
# print("\n")
# print("\n--------PRUEBA 12--------\n")       
# parse_test('pruebas/12.txt')
# print("\n")
# print("\n--------PRUEBA 13--------\n")       
# parse_test('pruebas/13.txt')
# print("\n")


# Pruebas 2da entrega 
print("\n\nAnalizador detecta todos los errores en las entradas dadas.")
print("\nAST para cada caso en carpeta pruebas2/ ")
print("\n--------PRUEBA 2.1--------\n")       
parse_test('pruebas2/1.txt')
print("\n")
print("\n--------PRUEBA 2.2--------\n")       
parse_test('pruebas2/2.txt')
print("\n")
print("\n--------PRUEBA 2.3--------\n")       
parse_test('pruebas2/3.txt')
print("\n")
print("\n--------PRUEBA 2.4--------\n")       
parse_test('pruebas2/4.txt')
print("\n")
print("\n--------PRUEBA 2.5--------\n")       
parse_test('pruebas2/5.txt')
print("\n")
print("\n--------PRUEBA 2.6--------\n")       
parse_test('pruebas2/6.txt')
print("\n")
print("\n--------PRUEBA 2.7--------\n")       
parse_test('pruebas2/7.txt')
print("\n")
print("\n--------PRUEBA 2.8--------\n")       
parse_test('pruebas2/8.txt')
print("\n")
print("\n--------PRUEBA 2.9--------\n")       
parse_test('pruebas2/9.txt')
print("\n")
print("\n--------PRUEBA 2.10--------\n")       
parse_test('pruebas2/10.txt')
print("\n")
print("\n--------PRUEBA 2.11--------\n")       
parse_test('pruebas2/11.txt')
print("\n")