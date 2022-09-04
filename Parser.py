from Errors import InvalidSyntaxError
from Tokens import *
###############################
# NODES
###############################

class NumberNode:
	def __init__(self, tok):
		self.tok = tok

		self.pos_start = self.tok.pos_start
		self.pos_end = self.tok.pos_end

	def __repr__(self):
		return str(self.tok)

class StringNode:
	def __init__(self, tok):
		self.tok = tok

		self.pos_start = self.tok.pos_start
		self.pos_end = self.tok.pos_end

	def __repr__(self):
		return str(self.tok)

class ListNode:
	def __init__(self, element_nodes, pos_start, pos_end, is_multi=False):
		self.element_nodes = element_nodes
		self.is_multi = is_multi

		self.pos_start = pos_start
		self.pos_end = pos_end	

class BoolNode:
	def __init__(self, tok):
		self.tok = tok

		self.pos_start = self.tok.pos_start
		self.pos_end = self.tok.pos_end

	def __repr__(self):
		return str(self.tok)

class UnaryOpNode:
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node

		self.pos_start = self.op_tok.pos_start
		self.pos_end = node.pos_end

	def __repr__(self):
		return '(' + str(self.op_tok) + str(self.node) + ')'

class BinOpNode:
	def __init__(self, left_node, op_tok, right_node):
		self.left_node = left_node
		self.op_tok = op_tok
		self.right_node = right_node

		self.pos_start = self.left_node.pos_start
		self.pos_end = self.right_node.pos_end

	def __repr__(self):
		return '(' + str(self.left_node) + ',' + str(self.op_tok) + ',' + str(self.right_node) + ')'

class IfNode:
	def __init__(self, cases, else_case):
		self.cases = cases
		self.else_case = else_case

		self.pos_start = self.cases[0][0].pos_start
		self.pos_end = (self.else_case or self.cases[len(self.cases) -1 ])[0].pos_end

class ForNode:
	def __init__(self, var_name_tok, start_value_node, end_value_node, inc_value_node, body_node, should_return_null):
		self.var_name_tok = var_name_tok
		self.start_value_node = start_value_node
		self.end_value_node = end_value_node
		self.inc_value_node = inc_value_node
		self.body_node = body_node
		self.should_return_null = should_return_null

		self.pos_start = self.var_name_tok.pos_start
		self.pos_end = self.body_node.pos_end

class WhileNode:
		def __init__(self, condition_node, body_node, should_return_null):
			self.condition_node = condition_node
			self.body_node = body_node
			self.should_return_null = should_return_null

			self.pos_start = self.condition_node.pos_start
			self.pos_end = self.body_node.pos_end

class VarAccessNode:
	def __init__(self, var_name_tok):
		self.var_name_tok = var_name_tok

		self.pos_start = self.var_name_tok.pos_start
		self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
	def __init__(self, var_name_tok, value_node):
		self.var_name_tok = var_name_tok
		self.value_node = value_node

		self.pos_start = self.var_name_tok.pos_start
		self.pos_end = self.var_name_tok.pos_end
			
class FuncDefNode:
		def __init__(self, var_name_tok, arg_name_toks, body_node, should_auto_return):
			self.var_name_tok = var_name_tok
			self.arg_name_toks = arg_name_toks
			self.body_node = body_node
			self.should_auto_return = should_auto_return

			if self.var_name_tok:
				self.pos_start = self.var_name_tok.pos_start
			elif len(self.arg_name_toks) > 0:
				self.pos_start = self.arg_name_toks[0].pos_start
			else:
				self.pos_start = self.body_node.pos_start

			self.pos_end = self.body_node.pos_end

class CallNode:
	def __init__(self, node_to_call, arg_nodes):
		self.node_to_call = node_to_call
		self.arg_nodes = arg_nodes

		self.pos_start = self.node_to_call.pos_start

		if len(self.arg_nodes) > 0:
			self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
		else:
			self.pos_end = self.node_to_call.pos_end

class ReturnNode:
	def __init__(self, node_to_return, pos_start, pos_end):
		self.node_to_return = node_to_return

		self.pos_start = pos_start
		self.pos_end = pos_start

class ContinueNode:
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end


class BreakNode:
	def __init__(self, pos_start, pos_end):
		self.pos_start = pos_start
		self.pos_end = pos_end
		

###############################
# PARSE RESULT
###############################

class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
		self.last_registered_advance_count = 0
		self.advance_count = 0
		self.to_reverse_count = 0

	def register_advancement(self):
		self.last_registered_advance_count = 1
		self.advance_count += 1

	def register(self, res):
		self.last_registered_advance_count = 1
		self.advance_count += res.advance_count
		if res.error: self.error = res.error
		return res.node

	def try_register(self, res):
		if res.error:
			self.to_reverse_count = res.advance_count
			return None
		return self.register(res)
	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
		if not self.error or self.advance_count == 0:
			self.error = error
		return self
		
###############################
# PARSER
###############################

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.tok_idx = -1
		self.advance()

	def advance(self, ):
		self.tok_idx += 1
		self.update_current_tok()
		return self.current_tok

	def reverse(self, amount=1):
		self.tok_idx -= amount
		self.update_current_tok()
		return self.current_tok

	def update_current_tok(self):
		if self.tok_idx < len(self.tokens):
			self.current_tok = self.tokens[self.tok_idx]

	def parse(self):
		res = self.statements()
		if not res.error and self.current_tok.type != TT_EOF:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '+', '-', '*', or '/'"
			))
		return res

	###########################################
	def statements(self):
		res = ParseResult()
		statements = []
		pos_start = self.current_tok.pos_start.copy()

		while self.current_tok.type == TT_NEWLINE:
			res.register_advancement()
			self.advance()

		statement = res.register(self.statement())
		if res.error: return res
		statements.append(statement)

		more_statements = True

		while True:
			newline_count = 0
			
			while self.current_tok.type == TT_NEWLINE:
				res.register_advancement()
				self.advance()
				newline_count += 1
			if newline_count == 0:
				more_statements = False

			if not more_statements: break
			statement = res.try_register(self.statement())
			if not statement:
				self.reverse(res.to_reverse_count)
				more_statements = False
				continue
			statements.append(statement)

		return res.success(ListNode(
			statements,
			pos_start,
			self.current_tok.pos_end.copy(),
			True
		))

	def statement(self):
		res = ParseResult()
		pos_start = self.current_tok.pos_start.copy()

		if self.current_tok.matches(TT_KEYWORD, 'return'):
			res.register_advancement()
			self.advance()

			expr = res.try_register(self.expr())
			if not expr:
				self.reverse(res.to_reverse_count)
			return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))


		if self.current_tok.matches(TT_KEYWORD, 'continue'):
			res.register_advancement()
			self.advance()
			return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

		if self.current_tok.matches(TT_KEYWORD, 'break'):
			res.register_advancement()
			self.advance()
			return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

		expr = res.register(self.expr())
		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected 'var', 'return', 'continue', 'break', number, identifier, 'if', 'for', 'while', 'def', '+', '-', '(', '[',  or 'not'"
			))

		return res.success(expr)
			
	def for_expr(self):
		res = ParseResult()

		if not self.current_tok.matches(TT_KEYWORD, 'for'):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected 'for'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type != TT_IDENTIFIER:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected identifier"
			))

		var_name = self.current_tok
		res.register_advancement()
		self.advance()

		if self.current_tok.type != TT_EQUALS:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '='"
			))

		res.register_advancement()
		self.advance()

		start_value = res.register(self.expr())
		if res.error:return res

		if not self.current_tok.matches(TT_KEYWORD, 'to'):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected 'to'"
			))

		res.register_advancement()
		self.advance()

		end_value = res.register(self.expr())
		if res.error: return res

		if self.current_tok.matches(TT_KEYWORD, 'inc'):
			res.register_advancement()
			self.advance()

			inc_value = res.register(self.expr())
			if res.error: return res
		else:
			inc_value = None


		if self.current_tok.type != TT_LCURLY:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '{'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_NEWLINE:
			res.register_advancement()
			self.advance()

			body = res.register(self.statements())
			if res.error: return res

			if not self.current_tok.type == TT_RCURLY:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '}'"
				))

			res.register_advancement()
			self.advance()

			return res.success(ForNode(var_name, start_value, end_value, inc_value, body, True))

		body = res.register(self.statement())
		if res.error: return res

		return res.success(ForNode(var_name, start_value, end_value, inc_value, body, False))

	def while_expr(self):
		res = ParseResult()

		if not self.current_tok.matches(TT_KEYWORD, 'while'):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected 'while'"
			))

		res.register_advancement()
		self.advance()

		condition = res.register(self.expr())
		if res.error: return res

		if self.current_tok.type != TT_LCURLY:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '{'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_NEWLINE:
			res.register_advancement()
			self.advance()
			body = res.register(self.statements())
			if res.error: return res

			if not self.current_tok.type == TT_RCURLY:
				return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '}'"
			))

			res.register_advancement()
			self.advance()

			return res.success(WhileNode(condition, body, True))

		body = res.register(self.statement())
		if res.error: return res

		return res.success(WhileNode(condition, body, False))		

	def list_expr(self):
		res = ParseResult()
		element_nodes = []
		pos_start = self.current_tok.pos_start.copy()
		
		if self.current_tok.type != TT_LSQUARE:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '['"
				))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_RSQUARE:
			res.register_advancement()
			self.advance()
		else:
			element_nodes.append(res.register(self.expr()))
			if res.error:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ']' ,'var', int, float, identifier, '+', '-', '(', '[' or 'not'"
				))

			while self.current_tok.type == TT_COMMA:
				res.register_advancement()
				self.advance()

				element_nodes.append(res.register(self.expr()))
				if res.error: return res

			if self.current_tok.type != TT_RSQUARE:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ',' or ']'"
				))

			res.register_advancement()
			self.advance()

		return res.success(ListNode(
			element_nodes,
			pos_start,
			self.current_tok.pos_end.copy()
		))
		
	def if_expr(self):
		res = ParseResult()
		all_cases = res.register(self.if_expr_cases('if'))

		if res.error: return res
		cases, else_case = all_cases

		return res.success(IfNode(cases, else_case))

	def if_expr_b(self):
		return self.if_expr_cases('elif')

	def if_expr_c(self):
		res = ParseResult()
		else_case = None

		if self.current_tok.matches(TT_KEYWORD, 'else'):
			res.register_advancement()
			self.advance()

			if self.current_tok.type != TT_LCURLY:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '{'"
				))

			res.register_advancement()
			self.advance()

			if self.current_tok.type == TT_NEWLINE:
				res.register_advancement()
				self.advance()

				statements = res.register(self.statements())

				if res.error: return res
				else_case = (statements, True)

				if self.current_tok.type == TT_RCURLY:
					res.register_advancement()
					self.advance()
				else:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						"Expected '}'"
					))
			else:
				expr = res.register(self.statement())
				if res.error: return res
				else_case = (expr, False)

		return res.success(else_case)

	def if_expr_b_or_c(self):
		res = ParseResult()
		cases, else_case = [], None

		if self.current_tok.matches(TT_KEYWORD, 'elif'):
			all_cases = res.register(self.if_expr_b())
			if res.error: return res
			cases, else_case = all_cases
		else:
			else_case = res.register(self.if_expr_c())
			if res.error: return res

		return res.success((cases, else_case))

	def if_expr_cases(self, case_keyword):
		res = ParseResult()
		cases = []
		else_case = None

		if not self.current_tok.matches(TT_KEYWORD, case_keyword):
			return res.failure(InvalidSyntaxError(
			self.current_tok.pos_start, self.current_tok.pos_end,
			"Expected '" + str(case_keyword) + "'"
		))

		res.register_advancement()
		self.advance()

		condition = res.register(self.expr())
		if res.error: return res

		if self.current_tok.type != TT_LCURLY:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '{'"
		))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_NEWLINE:
			res.register_advancement()
			self.advance()

			statements = res.register(self.statements())
			if res.error: return res
			cases.append((condition, statements, True))

			if self.current_tok.type != TT_RCURLY:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '}'"
				))
			res.register_advancement()
			self.advance()
			if self.current_tok.type == TT_NEWLINE:
				res.register_advancement()
				self.advance()
			if self.current_tok.matches(TT_KEYWORD, 'elif') or self.current_tok.matches(TT_KEYWORD, 'else'):
				all_cases = res.register(self.if_expr_b_or_c())

				if res.error: return res
				new_cases, else_case = all_cases
				cases.extend(new_cases)
		else:
			expr = res.register(self.statement())
			if res.error: return res
			cases.append((condition, expr, False))

			all_cases = res.register(self.if_expr_b_or_c())
			if res.error: return res
			new_cases, else_case = all_cases
			cases.extend(new_cases)

		return res.success((cases, else_case))

	def power(self):
		return self.bin_op(self.call, (TT_POWER, ), self.factor)

	def call(self):
		res = ParseResult()
		atom = res.register(self.atom())
		if res.error: return res


		if self.current_tok.type == TT_LPAREN:
			res.register_advancement()
			self.advance()
			arg_nodes = []

			if self.current_tok.type == TT_RPAREN:
				res.register_advancement()
				self.advance()
			else:
				arg_nodes.append(res.register(self.expr()))
				if res.error:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						"Expected ')', 'var', 'if', 'for', 'while', 'def', int, float, identifier, '+', '-',  '(', '[', or 'not'"
					))

				while self.current_tok.type == TT_COMMA:
					res.register_advancement()
					self.advance()

					arg_nodes.append(res.register(self.expr()))
					if res.error: return res

				if self.current_tok.type != TT_RPAREN:
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						"Expected ',' or ')'"
					))

				res.register_advancement()
				self.advance()

			return res.success(CallNode(atom, arg_nodes))
		return res.success(atom)

	def atom(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_INT, TT_FLOAT):
			res.register_advancement()
			self.advance()
			return res.success(NumberNode(tok))

		if tok.type == TT_STRING:
			res.register_advancement()
			self.advance()
			return res.success(StringNode(tok))

		elif tok.type == TT_IDENTIFIER:
			res.register_advancement()
			self.advance()
			return res.success(VarAccessNode(tok))

		elif tok.type == TT_LPAREN:
			res.register_advancement()
			self.advance()
			expr = res.register(self.expr())
			if res.error: return res
			if self.current_tok.type == TT_RPAREN:
				res.register_advancement()
				self.advance()
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected ')'"
				))

		elif tok.type == TT_LSQUARE:
			list_expr = res.register(self.list_expr())
			if res.error: return res
			return res.success(list_expr)


		elif tok.matches(TT_KEYWORD, 'if'):
			if_expr = res.register(self.if_expr())
			if res.error: return res
			return res.success(if_expr)

		elif tok.matches(TT_KEYWORD, 'for'):
			for_expr = res.register(self.for_expr())
			if res.error: return res
			return res.success(for_expr)

		elif tok.matches(TT_KEYWORD, 'while'):
			while_expr = res.register(self.while_expr())
			if res.error: return res
			return res.success(while_expr)

		elif tok.matches(TT_KEYWORD, 'def'):
			def_expr = res.register(self.func_def())
			if res.error: return res
			return res.success(def_expr)

		return res.failure(InvalidSyntaxError(
				tok.pos_start, tok.pos_end,
				"Expected int, float, identifier, '+', '-', '(', '[', 'if', 'for', 'while', or 'def'"
			))

	def factor(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_PLUS, TT_MINUS):
			res.register_advancement()
			self.advance()
			factor = res.register(self.factor())
			if res.error: return res
			return res.success(UnaryOpNode(tok, factor))

		return self.power()

	def term(self):
		return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD))

	def arith_expr(self):
		return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

	def comp_expr(self):
		res = ParseResult()

		if self.current_tok.matches(TT_KEYWORD, 'not'):
			op_tok = self.current_tok
			res.register_advancement()
			self.advance()

			node = res.register(self.comp_expr())
			if res.error: return res
			return res.success(UnaryOpNode(op_tok, node))

		node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected int, float, identifier, '+', '-', '(', '[', or 'not"
			))

		return res.success(node)

	def expr(self):
		res = ParseResult()

		if self.current_tok.matches(TT_KEYWORD, 'var'):
			res.register_advancement()
			self.advance()

			if self.current_tok.type != TT_IDENTIFIER:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected identifier"
				))

			var_name = self.current_tok
			res.register_advancement()
			self.advance()

			if self.current_tok.type != TT_EQUALS:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '='"
				))

			res.register_advancement()
			self.advance()
			expr = res.register(self.expr())
			if res.error: return res

			return  res.success(VarAssignNode(var_name, expr))

		node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, "and"), (TT_KEYWORD, "or"))))

		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected 'var', int, float, identifier, 'if', 'for', 'while', 'def', '+', '-', '(', '[',  or 'not'"
			))

		return res.success(node)

	def func_def(self):
		res = ParseResult()

		if not self.current_tok.matches(TT_KEYWORD, 'def'):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected 'def'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TT_IDENTIFIER:
			var_name_tok = self.current_tok
			res.register_advancement()
			self.advance()
			if self.current_tok.type != TT_LPAREN: 
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '('"
				))
		else:
			var_name_tok = None
			if self.current_tok.type != TT_LPAREN:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected identifier or '('"
				))

		res.register_advancement()
		self.advance()
		arg_name_toks = []

		if self.current_tok.type == TT_IDENTIFIER:
			arg_name_toks.append(self.current_tok)
			res.register_advancement()
			self.advance()

			while self.current_tok.type == TT_COMMA:
				res.register_advancement()
				self.advance()

				if self.current_tok.type != TT_IDENTIFIER: 
					return res.failure(InvalidSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						"Expected identifier"
					))

				arg_name_toks.append(self.current_tok)
				res.register_advancement()
				self.advance()

			if self.current_tok.type != TT_RPAREN:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ',' or ')'"
				))
		else:
			if self.current_tok.type != TT_RPAREN:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected identifier or ')'"
				))

		res.register_advancement()
		self.advance()


		if self.current_tok.type != TT_LCURLY:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '{'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type != TT_NEWLINE:
			res.register_advancement()
			self.advance()
		
			body = res.register(self.expr())
			if res.error: return res

			if self.current_tok.type != TT_RCURLY:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '}'"
				))

			res.register_advancement()
			self.advance()

			return res.success(FuncDefNode(
				var_name_tok, 
				arg_name_toks,
				body,
				True
			))

		res.register_advancement()
		self.advance()

		body = res.register(self.statements())
		if res.error: return res

		if self.current_tok.type != TT_RCURLY:
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '}'"
			))

		res.register_advancement()
		self.advance()

		return res.success(FuncDefNode(
			var_name_tok,
			arg_name_toks,
			body,
			False
		))

	def bin_op(self, func_a, ops, func_b=None):
		if func_b == None:
			func_b = func_a

		res = ParseResult()
		left = res.register(func_a())
		if res.error: return res

		while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
			op_tok = self.current_tok
			res.register_advancement()
			self.advance()
			right = res.register(func_b())
			if res.error: return res
			left = BinOpNode(left, op_tok, right)

		return res.success(left)


if __name__ == '__main__':
	import Lexer
	tokens = Lexer.tokens
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: print(ast.error)
	elif ast: print(ast)