# -*- coding: utf-8 -*-
import re

import re

# Lexer: convierte el código en tokens
def lexer(code):
    token_specification = [
        ('NUMBER',   r'\d+'),            # Números enteros
        ('ID',       r'[A-Za-z]+'),      # Identificadores (variables como "a")
        ('ASSIGN',   r'='),              # Operador de asignación
        ('SEMICOLON', r';'),             # Punto y coma
        ('OP',       r'[+\-*/]'),        # Operadores
        ('SKIP',     r'[ \t]+'),         # Espacios en blanco
        ('MISMATCH', r'.'),              # Cualquier otro carácter no esperado
    ]

    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_type, regex in token_specification:
            pattern = re.compile(regex)
            match = pattern.match(code, pos)
            if match:
                text = match.group(0)
                if token_type == 'SKIP':
                    pass  # Ignora espacios en blanco
                elif token_type == 'MISMATCH':
                    raise ValueError("Unexpected character '{}' at position {}".format(text, pos))
                else:
                    tokens.append((token_type, text))
                pos = match.end(0)
                break
        if not match:
            raise ValueError("Unexpected character '{}' at position {}".format(code[pos], pos))
    return tokens

# AST Node
class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if self.tokens[self.pos][0] == 'ID' and self.tokens[self.pos + 1][0] == 'ASSIGN':
            left = Node('ID', self.tokens[self.pos][1])
            self.pos += 2  # Skip ID and ASSIGN
            right = self.expression()
            return Node('ASSIGN', left=left, right=right)

    def expression(self):
        left = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] in ('+', '-'):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.term()
            left = Node(op[0], value=op[1], left=left, right=right)
        return left

    def term(self):
        token = self.tokens[self.pos]
        self.pos += 1
        if token[0] == 'NUMBER':
            return Node('NUMBER', value=int(token[1]))
        elif token[0] == 'ID':
            return Node('ID', value=token[1])

# Semantic Analyzer
class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        if node.type == 'ASSIGN':
            var_name = node.left.value
            value_type = self.get_type(node.right)
            self.symbol_table[var_name] = value_type
        elif node.type in ('+', '-'):
            left_type = self.get_type(node.left)
            right_type = self.get_type(node.right)
            if left_type != 'int' or right_type != 'int':
                raise TypeError("Solo se permiten operaciones entre enteros.")
        print("Análisis semántico completado exitosamente.")

    def get_type(self, node):
        if node.type == 'NUMBER':
            return 'int'
        elif node.type == 'ID':
            if node.value not in self.symbol_table:
                raise NameError("Variable '{}' no está definida.".format(node.value))
            return self.symbol_table[node.value]

# Ejecución del Analizador
code = "a = 5 + 3;"  # Puedes cambiar el código de prueba aquí
tokens = lexer(code)
print("Tokens:", tokens)
parser = Parser(tokens)
ast = parser.parse()
print("AST:", ast)
semantic_analyzer = SemanticAnalyzer()
semantic_analyzer.analyze(ast)
