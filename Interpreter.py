import string, math, random
from Errors import RTError
from Tokens import *

###############################
# RUNTIME RESULT
###############################

class RTResult:
	def __init__(self):
		self.reset()

	def reset(self):
		self.value = None
		self.error = None
		self.func_return_value = None
		self.loop_should_continue = False
		self.loop_should_break = False

	def register(self, res):
		self.error = res.error
		self.func_return_value = res.func_return_value
		self.loop_should_break = res.loop_should_break
		self.loop_should_continue = res.loop_should_continue
		return res.value

	def success(self, value):
		self.reset()
		self.value = value
		return self

	def success_return(self, value):
		self.reset()
		self.func_return_value = value
		return self

	def success_continue(self):
		self.reset()
		self.loop_should_continue = True
		return self

	def success_break(self):
		self.reset()
		self.loop_should_break = True
		return self


	def failure(self, error):
		self.reset()
		self.error = error
		return self

	def should_return(self):
		return (
			self.error or
			self.func_return_value or
			self.loop_should_continue or
			self.loop_should_break
		)

###############################
# VALUES
###############################

class Value:
	def __init__(self):
		self.set_pos()
		self.set_context()

	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def added_to(self, other):
		return None, self.illegal_operation(other)

	def subbed_by(self, other):
		return None, self.illegal_operation(other)
		
	def multiplied_by(self, other):
		return None, self.illegal_operation(other)
		
	def divided_by(self, other):
		return None, self.illegal_operation(other)
		
	def power_of(self, other):
		return None, self.illegal_operation(other)
		
	def mod_of(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_eq(self, other):
		return None, self.illegal_operation(other)
		
	def get_comparison_ne(self, other):
		return None, self.illegal_operation(other)
		
	def get_comparison_lt(self, other):
		return None, self.illegal_operation(other)
		
	def get_comparison_gt(self, other):
		return None, self.illegal_operation(other)
		
	def get_comparison_lte(self, other):
		return None, self.illegal_operation(other)
		
	def get_comparison_gte(self, other):
		return None, self.illegal_operation(other)
		
	def anded_by(self, other):
		return None, self.illegal_operation(other)
		
	def ored_by(self, other):
		return None, self.illegal_operation(other)
		
	def execute(self, args):
		return RTResult().failure(self.illegal_operation())

		
	def illegal_operation(self, other=None):
		if not other: other = self
		return RTError(
			self.pos_start, other.pos_end,
			'Illegal operation,',
			self.context
		)
		
class Number(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def subbed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def multiplied_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def divided_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end,
					"ZeroDivisionError",
					self.context
					)
			return Number(self.value / other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def power_of(self, other):
		if isinstance(other, Number):
			return Number(self.value ** other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)
		
	def mod_of(self, other):
		if isinstance(other, Number):
			return Number(self.value % other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)


	def get_comparison_eq(self, other):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(self.value == other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def get_comparison_ne(self, other):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(self.value != other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def get_comparison_lt(self, other):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(self.value < other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def get_comparison_gt(self, other):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(self.value > other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def get_comparison_lte(self, other):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(self.value <= other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def get_comparison_gte(self, other):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(self.value >= other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)


	def anded_by(self, other):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(self.value and other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def ored_by(self, other):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(self.value or other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def notted(self):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(True if self.value == 0 else False).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def is_true(self):
		return self.value != 0

	def __repr__(self):
		return str(self.value)

class Bool(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def copy(self):
		copy = Bool(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def get_comparison_eq(self, other):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(self.value == bool(other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def get_comparison_ne(self, other):
		if isinstance(other, Number) or isinstance(other, Bool):
			return Bool(bool(self.value) != other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def is_true(self):
		return self.value != False

	def __repr__(self):
		return str(self.value).lower()

Number.null = Number(0)
Bool.true = Bool(True)
Bool.false = Bool(False)
Number.pi = Number(3.14159265)
Number.pi_precise = Number(3.141592653589793)

class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def added_to(self, other):
		if isinstance(other, String):
			return String(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def multiplied_by(self, other):
		if isinstance(other, Number):
			return String(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_eq(self, other):
		if isinstance(other, String):
			return Bool(self.value == str(other.value)).set_context(self.context), None
		else:	
			return None, Value.illegal_operation(self.pos_start, other.pos_end)

	def is_true(self, other):
		return len(self.value) > 0

	def copy(self):
		copy = String(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __str__(self):
		return self.value

	def __repr__(self):
		return '"' + str(self.value) + '"'

class List(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements

	def added_to(self, other):
		new_list = self.copy()
		new_list.elements.append(other)
		return new_list, None

	def subbed_by(self, other):
		if isinstance(other, Number):
			new_list = self.copy()
			try:
				new_list.elements.pop(other.value)
				return new_list, None
			except:
				return None, RTError(
					other.pos_start, other.pos_end,
					"Element index is out of range",
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)

	def multiplied_by(self, other):
		if isinstance(other, List):
			new_list = self.copy()
			new_list.elements.extend(other.elements)
			return new_list, None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lt(self, other):
		if isinstance(other, Number):
			try:
				return self.elements[other.value], None
			except:
				return None, RTError(
					other.pos_start, other.pos_end,
					"Element index is out of range",
					self.context
				)
		else:
			return None, Value.illegal_operation(self, other)

	def copy(self):
		copy = List(self.elements)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __repr__(self):
		return '[' + ', '.join([str(x) for x in self.elements]) + ']'

class BaseFunction(Value):
	def __init__(self, name):
		super().__init__()
		self.name = name or '<anonymous>'

	def generate_new_context(self):
		new_context = Context(self.name, self.context, self.pos_start)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
		return new_context

	def check_args(self, arg_names, args):
		res = RTResult()

		if len(args) != len(arg_names):
			return res.failure(RTError(
				self.pos_start, self.pos_end,
				"Expected " + str(len(arg_names)) + " arguments but " + str(len(args)) + " where given",
				self.context
			))

		return res.success(None)

	def populate_args(self, arg_names, args, exec_ctx):
		for i in range(len(args)):
			arg_name = arg_names[i]
			arg_value = args[i]
			arg_value.set_context(exec_ctx)
			exec_ctx.symbol_table.set(arg_name, arg_value)

	def check_and_populate_args(self, arg_names, args, exec_ctx):
		res = RTResult()
		res.register(self.check_args(arg_names, args))
		if res.should_return(): return res
		self.populate_args(arg_names, args, exec_ctx)
		return res.success(None)
 
class Function(BaseFunction):
	def __init__(self, name, body_node, arg_names, should_auto_return):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names
		self.should_auto_return = should_auto_return

	def execute(self, args):
		res = RTResult()
		interpreter = Interpreter()
		exec_ctx = self.generate_new_context()

		res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
		if res.should_return(): return res

		value = res.register(interpreter.visit(self.body_node, exec_ctx))
		if res.should_return() and res.func_return_value == None: return res
		ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
		return res.success(ret_value)

	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return '<function ' + str(self.name) + '>'

class BuiltInFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)

	def execute(self, args):
		res = RTResult()
		exec_ctx = self.generate_new_context()

		method_name = 'execute_' + str(self.name)
		method = getattr(self, method_name, self.no_visit_method)

		res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
		if res.should_return(): return res

		return_value =  res.register(method(exec_ctx))
		if res.should_return(): return res
		return res.success(return_value)

	def no_visit_method(self, node, context):
		raise Exception('No execute_' + str(self.name) + ' method defined')

	def copy(self):
		copy = BuiltInFunction(self.name)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return '<built-in function ' + self.name + '>'

	####################################################

	# Console
	def execute_wrt(self, exec_ctx):
		print(String(str(exec_ctx.symbol_table.get('value'))))
		return RTResult().success(Number.null)
	execute_wrt.arg_names = ['value']

	def execute_input(self, exec_ctx):
		text = str(input())
		return RTResult().success(String(text))
	execute_input.arg_names = []

	# Data types
	def execute_type(self, exec_ctx):
		if isinstance(exec_ctx.symbol_table.get("value"), Number): 
			return RTResult().success(String("Int"))
		elif isinstance(exec_ctx.symbol_table.get("value"), String):
			return RTResult().success(String("Str"))
		elif isinstance(exec_ctx.symbol_table.get("value"), List):
			return RTResult().success(String("List"))
		elif isinstance(exec_ctx.symbol_table.get("value"), Function):
			return RTResult().success(String("Function"))
		elif isinstance(exec_ctx.symbol_table.get("value"), BuiltInFunction):
			return RTResult().success(String("BuiltInFunction"))
	execute_type.arg_names = ['value']

	def execute_int(self, exec_ctx):
		value = exec_ctx.symbol_table.get("value")
		try:
			return RTResult().success(Number(int(value.value)))
		except:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Could not convert to int",
				exec_ctx
			))
	execute_int.arg_names = ['value']

	def execute_str(self, exec_ctx):
		value = exec_ctx.symbol_table.get("value")
		try:
			return RTResult().success(String(str(value.value)))
		except:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Could not convert to str",
				exec_ctx
			))
	execute_str.arg_names = ['value']


	def execute_float(self, exec_ctx):
		value = exec_ctx.symbol_table.get("value")
		try:
			return RTResult().success(Number(float(value.value)))
		except:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Could not convert to float",
				exec_ctx
			))
	execute_float.arg_names = ['value']

	def execute_bin(self, exec_ctx):
		int_ = exec_ctx.symbol_table.get("int")
		try:
			return RTResult().success(String(bin(int_.value)))
		except:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Could not convert to binary",
				exec_ctx
			))
	execute_bin.arg_names = ['int']

	def execute_hex(self, exec_ctx):
		int_ = exec_ctx.symbol_table.get("int")
		try:
			return RTResult().success(String(hex(int_.value)))
		except:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Could not convert to binary",
				exec_ctx
			))
	execute_hex.arg_names = ['int']

	def execute_length(self, exec_ctx):
		value = exec_ctx.symbol_table.get("value")
		try:
			return RTResult().success(Number(len(value.value)))
		except:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Could not get length",
				exec_ctx
			))
	execute_length.arg_names = ['value']

	# Lists
	def execute_append(self, exec_ctx):
		list_ = exec_ctx.symbol_table.get("list")
		value = exec_ctx.symbol_table.get("value")

		if not isinstance(list_, List):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"First argument must be of type List",
				exec_ctx
			))

		list_.elements.append(value)
		return RTResult().success(Number.null)
	execute_append.arg_names = ['list', 'value']

	def execute_pop(self, exec_ctx):
		list_ = exec_ctx.symbol_table.get("list")
		idx = exec_ctx.symbol_table.get("idx")

		if not isinstance(list_, List):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"First argument must be of type List",
				exec_ctx
			))

		if not isinstance(idx, Number):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Second argument must be of type Number",
				exec_ctx
			))

		try:
			element = list_.elements.pop(idx.value)
		except:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"List index out of range",
				exec_ctx
			))
		return RTResult().success(element)
	execute_pop.arg_names = ['list', 'idx']

	def execute_extend(self, exec_ctx):
		listA = exec_ctx.symbol_table.get("listA")
		listB = exec_ctx.symbol_table.get("listB")

		if not isinstance(listA, List):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"First argument must be of type List",
				exec_ctx
			))

		if not isinstance(listB, List):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Second argument must be of type List",
				exec_ctx
			))

		listA.elements.extend(listB.elements)
		return RTResult().success(Number.null)
	execute_extend.arg_names = ['listA', 'listB']

	# Math
	def execute_abs(self, exec_ctx):
		int_ = exec_ctx.symbol_table.get("int")

		if not isinstance(int_, Number):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Must be Int",
				exec_ctx
			))

		if int_.value > 0:
			return RTResult().success(Number(int_.value))
		else:
			return RTResult().success(Number(int_.value*-1))
	execute_abs.arg_names = ['int']

	def execute_sqrt(self, exec_ctx):
		int_ = exec_ctx.symbol_table.get("int")
		
		if not isinstance(int_, Number):
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Must be Int",
				exec_ctx
			))

		return RTResult().success(Number(math.sqrt(int_.value)))
	execute_sqrt.arg_names = ['int']
	
	def execute_randomint(self, exec_ctx):
		StartInt = exec_ctx.symbol_table.get("StartInt")
		EndInt = exec_ctx.symbol_table.get("EndInt")

		try:
			return RTResult().success(Number(random.randint(StartInt.value, EndInt.value)))
		except:
			return RTResult().failure(RTError(
				self.pos_start, self.pos_end,
				"Could not generate random number based on arguments",
				exec_ctx
			))

	execute_randomint.arg_names = ['StartInt', 'EndInt']

BuiltInFunction.wrt				= BuiltInFunction("wrt")
BuiltInFunction.input  			= BuiltInFunction("input")

BuiltInFunction.type			= BuiltInFunction("type")
BuiltInFunction.int 			= BuiltInFunction("int")
BuiltInFunction.str 			= BuiltInFunction("str")
BuiltInFunction.bin 			= BuiltInFunction("bin")
BuiltInFunction.hex				= BuiltInFunction("hex")
BuiltInFunction.float 			= BuiltInFunction("float")
BuiltInFunction.length 			= BuiltInFunction("length")

BuiltInFunction.append			= BuiltInFunction("append")
BuiltInFunction.pop				= BuiltInFunction("pop")
BuiltInFunction.extend			= BuiltInFunction("extend")

BuiltInFunction.abs 			= BuiltInFunction("abs")
BuiltInFunction.sqrt 			= BuiltInFunction("sqrt")
BuiltInFunction.randomint 		= BuiltInFunction("randomint")

###############################
# CONTEXT
###############################

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None

###############################
# SYMBOL TABLE
###############################

class SymbolTable:
	def __init__(self, parent=None):
		self.symbols = {}
		self.parent = parent

	def get(self, name):
		value = self.symbols.get(name, None)
		if value == None and self.parent:
			return self.parent.get(name)

		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]

###############################
# INTERPRETER
###############################

class Interpreter:
	def visit(self, node, context):
		method_name = 'visit_' + str(type(node).__name__)
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node, context):
		raise Exception('No visit_' + str(type(node).__name__) + ' method defined')

	###############################

	def visit_NumberNode(self, node, context):
		return RTResult().success(
		Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_StringNode(self, node, context):
		return RTResult().success(
			String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_ListNode(self, node, context):
		res = RTResult()
		elements = []

		for element_node in node.element_nodes:
			elements.append(res.register(self.visit(element_node, context)))
			if res.should_return(): return res

		return res.success(
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
			)

	def visit_VarAccessNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_tok.value
		value = context.symbol_table.get(var_name)

		if not value:
			return res.failure(RTError(
				node.pos_start, node.pos_end,
				str(var_name) + " is not defined",
				context
				))

		value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return res.success(value)

	def visit_VarAssignNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_tok.value
		value = res.register(self.visit(node.value_node, context))
		if res.should_return(): return res

		context.symbol_table.set(var_name, value)
		return res.success(value)

	def visit_BinOpNode(self, node, context):
		res = RTResult()
		left = res.register(self.visit(node.left_node, context))
		if res.should_return(): return res
		right = res.register(self.visit(node.right_node, context))

		if node.op_tok.type == TT_PLUS:
			result, error = left.added_to(right)
		elif node.op_tok.type == TT_MINUS:
			result, error = left.subbed_by(right)
		elif node.op_tok.type == TT_MUL:
			result, error = left.multiplied_by(right)
		elif node.op_tok.type == TT_DIV:
			result, error = left.divided_by(right)
		elif node.op_tok.type == TT_POWER:
			result, error = left.power_of(right)
		elif node.op_tok.type == TT_MOD:
			result, error = left.mod_of(right)

		elif node.op_tok.type == TT_EE:
			result, error = left.get_comparison_eq(right)
		elif node.op_tok.type == TT_NE:
			result, error = left.get_comparison_ne(right)
		elif node.op_tok.type == TT_LT:
			result, error = left.get_comparison_lt(right)
		elif node.op_tok.type == TT_GT:
			result, error = left.get_comparison_gt(right)
		elif node.op_tok.type == TT_LTE:
			result, error = left.get_comparison_lte(right)
		elif node.op_tok.type == TT_GTE:
			result, error = left.get_comparison_gte(right)

		elif node.op_tok.matches(TT_KEYWORD, 'and'):
			result, error = left.anded_by(right)
		elif node.op_tok.matches(TT_KEYWORD, 'or'):
			result, error = left.ored_by(right)

		if error:
			return res.failure(error)
		else:
			return res.success(result.set_pos(node.pos_start, node.pos_end))

	def visit_UnaryOpNode(self, node, context):
		res = RTResult()
		number = res.register(self.visit(node.node, context))
		if res.should_return(): return res

		error = None

		if node.op_tok.type == TT_MINUS:
			number, error = number.multiplied_by(Number(-1))
		elif node.op_tok.matches(TT_KEYWORD, 'not'):
			number, error = number.notted()


		if error:
			return res.failure(error)
		else:
			return res.success(number.set_pos(node.pos_start, node.pos_end))

	def visit_IfNode(self, node, context):
		res = RTResult()

		for condition, expr, should_return_null in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.should_return(): return res

			if condition_value.is_true():
				expr_value = res.register(self.visit(expr, context))
				if res.should_return(): return res
				return res.success(Number.null if should_return_null else expr_value)

		if node.else_case:
			expr, should_return_null = node.else_case
			expr_value = res.register(self.visit(expr, context))
			if res.should_return(): return res
			return res.success(Number.null if should_return_null else expr_value)

		return res.success(Number.null)

	def visit_ForNode(self, node, context):
		res = RTResult()
		elements = []

		start_value = res.register(self.visit(node.start_value_node, context))
		if res.should_return(): return res

		end_value = res.register(self.visit(node.end_value_node, context))
		if res.should_return(): return res

		if node.inc_value_node:
			inc_value = res.register(self.visit(node.inc_value_node, context))
			if res.should_return(): return res
		else:
			inc_value = Number(1)

		i = start_value.value

		if inc_value.value >= 0:
			condition = lambda: i < end_value.value
		else:
			condition = lambda: i > end_value.value

		while condition():
			context.symbol_table.set(node.var_name_tok.value, Number(i))
			i += inc_value.value

			value = res.register(self.visit(node.body_node, context))
			if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

			if res.loop_should_continue:
				continue

			if res.loop_should_break:
				break

			elements.append(value)

		return res.success(None)

	def visit_WhileNode(self, node, context):
		res = RTResult()
		elements = []

		while True:
			condition = res.register(self.visit(node.condition_node, context))
			if res.should_return(): return res

			if not condition.is_true(): break

			value = res.register(self.visit(node.body_node, context))
			if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

			if res.loop_should_continue:
				continue

			if res.loop_should_break:
				break

			elements.append(value)

		return res.success(None)

	def visit_FuncDefNode(self, node, context):
		res = RTResult()

		func_name = node.var_name_tok.value if node.var_name_tok else None
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_toks]
		func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)

		if node.var_name_tok:
			context.symbol_table.set(func_name, func_value)

		return res.success(func_value)

	def visit_CallNode(self, node, context):
		res = RTResult()
		args = []

		value_to_call = res.register(self.visit(node.node_to_call, context))
		if res.should_return(): return res
		value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

		for arg_node in node.arg_nodes:
			args.append(res.register(self.visit(arg_node, context)))
			if res.should_return(): return res

		return_value = res.register(value_to_call.execute(args))
		if res.should_return(): return res
		return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return res.success(return_value)

	def visit_ReturnNode(self, node, context):
		res = RTResult()

		if node.node_to_return:
			value = res.register(self.visit(node.node_to_return, context))
			if res.should_return(): return res
		else:
			value = Number.null

		return res.success_return(value)

	def visit_ContinueNode(self, node, context):
		return RTResult().success_continue()

	def visit_BreakNode(self, node, context):
		return RTResult().success_break()

#################
# Built in func #
#################

global_symbol_table = SymbolTable()

# Console
global_symbol_table.set("wrt", BuiltInFunction.wrt)
global_symbol_table.set("input", BuiltInFunction.input)

# Data types
global_symbol_table.set("type", BuiltInFunction.type)
global_symbol_table.set("int", BuiltInFunction.int)
global_symbol_table.set("str", BuiltInFunction.str)
global_symbol_table.set("float", BuiltInFunction.float)
global_symbol_table.set("bin", BuiltInFunction.bin)
global_symbol_table.set("hex", BuiltInFunction.hex)
global_symbol_table.set("length", BuiltInFunction.length)

# Lists
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)

# Math
global_symbol_table.set("abs", BuiltInFunction.abs)
global_symbol_table.set("sqrt", BuiltInFunction.sqrt)
global_symbol_table.set("randomint", BuiltInFunction.randomint)

################
# Built in var #
################

global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("true", Bool.true)
global_symbol_table.set("false", Bool.false)
global_symbol_table.set("pi", Number.pi)
global_symbol_table.set("pi16", Number.pi_precise)
