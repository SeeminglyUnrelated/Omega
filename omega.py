from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter, Context, global_symbol_table
def run(fn, text):
	# Generate tokens
	lexer = Lexer(fn, text)
	tokens, error = lexer.make_tokens()

	if error: return None, error

	# Generate AST
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	# Run program
	interpreter = Interpreter()
	context = Context('<main>')

	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node, context)

	return result.value, result.error

#res, error = run("Test", 'def hi() { wrt("hello") }; hi()')
#if error: print(error.as_string())
#elif res: print(res)