def generate(ast: list) -> str:
    generated_code = ''
    #add " to the in the tokens generated. add syntax check in ast generation step
    for node in ast:
        if node.name == 'PrintNode':
            generated_code += f'print(f"{"".join([child.value for child in node.children])}")\n'
        if node.name == 'LetNode':
            generated_code += ''.join([child.value for child in node.children])+"\n"
    return generated_code
