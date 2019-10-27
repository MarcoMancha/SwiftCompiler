# Marco Antonio Mancha Alfaro A01206194
# Analizador lexico Swift

import ply.lex as lex
import ply.yacc as yacc

class MyLexer(object):

    # Definicion de tokens

    reserved = {
        'let': 'D_LET',
        'var': 'D_VAR',
        'else': 'S_ELSE',
        'while': 'S_WHILE',
        'if': 'S_IF',
        'False': 'E_FALSE',
        'True': 'E_TRUE',
        'readLine':'INPUT',
        'Int': 'class_INT',
        'Bool': 'class_BOOL',
        'Character': 'class_CHARACTER',
        'String': 'class_String',
        'print': 'OUTPUT',
        'class':'CLASS',
        'static':'STATIC',
        'func':'FUNCTION'
    }

    tokens = [  'ID', 'INT', 'ASSIGN', 'GREATER', 'GREATER_EQ', 'LESS','LESS_EQ', 'EQUAL', 'NOT_EQUAL',
                'LPAREN', 'RPAREN','LBRACE', 'RBRACE','LOG_AND','LOG_OR', 'COLON','SEMICOLON', 
                'STR_LITERAL', 'PLUS', 'MINUS', 'MULT', 'DIV', 'DOT'] + list(reserved.values())
    
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULT = r'\*'
    t_DIV = r'/'
    t_DOT = r'\.'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_ASSIGN = r'='
    t_LOG_AND = r'\&\&'
    t_LOG_OR = r'\|\|'
    t_GREATER = r'>'
    t_GREATER_EQ = r'>='
    t_LESS = r'<'
    t_LESS_EQ = r'<='
    t_EQUAL = r'=='
    t_NOT_EQUAL = r'!='

    # Definir variables auxiliares
    variables = [{}]
    classes = {}
    functions = {}
    index = 0

    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Definicion de expreciones regulares necesarias

    def t_COMMENT(self,t):
        r'\//.*'
        pass

    def t_ID(self,t):
        r'[#]?[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_INT(self,t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STR_LITERAL(self,t):
        r'"([^"\n]|(\\"))*"'
        return t

    t_ignore = " \t "

    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
