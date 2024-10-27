from dataclasses import dataclass
from tokenizer import Token
@dataclass
class PrintNode:
    name = 'PrintNode'
    children: list

@dataclass
class LetNode:
    name = "LetNode"
    children: list

@dataclass
class OperatorNode:
    name = 'OperatorNode'
    value: str

@dataclass
class SeparatorNode:
    name = 'SeparatorNode'
    value: str

@dataclass
class LiteralNode:
    name = 'LiteralNode'
    value: str
    
@dataclass
class IdentifierNode:
    name = 'IdentifierNode'
    value: str

def parse(tokens: list[Token]) -> list:
    ast = []
    i = 0
    while i < len(tokens):
        if tokens[i].type == 'KEYWORD':
            if tokens[i].value =='PRINT':
                ast.append(PrintNode([]))
                i+=1
                while tokens[i].value != ';':
                    if tokens[i].type == 'LITERAL':
                        ast[-1].children.append(LiteralNode(value = tokens[i].value))
                    if tokens[i].type == 'IDENTIFIER':
                        ast[-1].children.append(IdentifierNode(value = tokens[i].value))
                    if tokens[i].type == 'SEPARATOR':
                        ast[-1].children.append(SeparatorNode(value = tokens[i].value))
                    i+=1
            if tokens[i].value == 'LET':
                ast.append(LetNode([]))
                i+=1
                while tokens[i].value != ';':
                    if tokens[i].type == 'IDENTIFIER':
                        ast[-1].children.append(IdentifierNode(value = tokens[i].value))
                    if tokens[i].type == 'OPERATOR':
                        ast[-1].children.append(OperatorNode(value = tokens[i].value))
                    if tokens[i].type == 'SEPARATOR':
                        ast[-1].children.append(SeparatorNode(value = tokens[i].value))
                    if tokens[i].type == 'LITERAL':
                        ast[-1].children.append(LiteralNode(value = tokens[i].value))
                    i+=1
        i+=1
    return ast

def print_ast(ast: list):
    for node in ast:
        print(node.name)
        print('\t└── ', *node.children)