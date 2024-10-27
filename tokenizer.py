from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str

def tokenize(program: str) -> list[Token]:
    keywords = ["LET", "PRINT", "AND", "OR", "NOT", "IF", "ELSE", "GOTO"]
    separator = ['[', ']', '(', ')', '{', '}', ';', ',', '"']
    operator = ['+', '-', '*', '/', '%', '=', '!=', '>', '<', '==', '<=', '>=']
    tokens = []
    variables = set()
    count = 0
    lines = program.split(';')[:-1]

    def parse_string(string):
        tokens.append(Token("LITERAL", string[1:-1]))

    def parse_expression(expression):
        for e in expression:
            if e in separator:
                tokens.append(Token("SEPARATOR", e))
            elif e in operator:
                tokens.append(Token("OPERATOR", e))
            elif (e.isalpha()) and (e in variables):
                tokens.append(Token('IDENTIFIER', e))
            elif e.lstrip('-').isnumeric():
                tokens.append(Token("LITERAL", e))
            elif len(e.split('.')) == 2:
                if (e.split('.')[0].lstrip('-').isnumeric()) and (e.split('.')[1].lstrip('-').isnumeric()):
                    tokens.append(Token("LITERAL", e))
            else:
                if (e.isalpha()) and not(e in variables):
                    raise Exception(f"Variable {e} not defined")
                else:
                    raise Exception("Something wrong in the expression")

    def parse_print(string):
        assert string[0] == string[-1] == '"', "Error in PRINT. Missing \""
        if not(('{' in string) or ('}' in string)):
            parse_string(string)
        else:
            # strings with vars in a PRINT statement
            string = string[1:-1]
            start = 0
            for i, char in enumerate(string):
                if char == "{":
                    if len(string[start:i]):
                        tokens.append(Token("LITERAL", string[start:i]))
                    start = i + 1
                    tokens.append(Token("SEPARATOR", "{"))
                elif char == "}":
                    parse_expression(string[start:i])
                    tokens.append(Token("SEPARATOR", "}"))
                    start = i + 1
            
    def parse_let(expression):
        expression = expression.split('=')
        assert expression[0].isalpha(), "Invalid Variable name"
        if expression[0].isalpha():
            variables.add(expression[0])
            tokens.append(Token('IDENTIFIER', expression[0]))
            tokens.append(Token('OPERATOR', '='))
        if expression[-1].lstrip('-').isnumeric():
            tokens.append(Token("LITERAL", expression[-1]))
        else:
            try:
                if float(expression[-1]):
                    tokens.append(Token("LITERAL", expression[-1]))
            except ValueError:
                parse_expression(expression[-1])
                #tokens.append(Token("EXPRESSION", expression[-1]))   

    for line in lines:
        line = line.replace('\n', '')
        chunks = line.split(' ')
        if chunks[0] == "PRINT":
            tokens.append(Token("KEYWORD", chunks[0]))
            parse_print(' '.join(chunks[1:]))
        if chunks[0] == "LET":
            tokens.append(Token("KEYWORD", chunks[0]))
            parse_let(''.join(chunks[1:]))
        tokens.append(Token("SEPARATOR", ';'))
    return tokens