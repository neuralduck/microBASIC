#!/usr/bin/env python3
import sys
from tokenizer import tokenize
import parser
from codegen import generate
filename = sys.argv[-1]
assert filename != sys.argv[0], "provide a microBASIC file to compile"
try:
	with open(filename, "r") as f:
	    mbprog = f.read()
except Exception:
	print("something went wrong")

tokens = tokenize(mbprog)
ast = parser.parse(tokens)
#print(*tokens)
#parser.print_ast(ast)
pyprog = generate(ast)
exec(pyprog)