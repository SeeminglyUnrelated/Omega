from Errors import IllegalCharError, ExpectedCharError
import string
from Tokens import *

###############################
# CONSTANTS
###############################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

###############################
# POSITION
###############################

class Position:
	def __init__(self, idx, ln, col, fn, ftxt):
		self.idx = idx
		self.ln = ln
		self.col = col
		self.fn = fn
		self.ftxt = ftxt

	def advance(self, current_char = None):
		self.idx += 1
		self.col += 1

		if current_char == "\n":
			self.ln += 1
			self.col = 0

		return self

	def copy(self):
		return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


###############################
# LEXER
###############################

class Lexer:
	def __init__(self, fn, text):
		self.fn = fn
		self.text = text
		self.pos = Position(-1, 0, -1, fn, text)
		self.current_char = None
		self.advance()

	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

	def make_tokens(self):
		tokens = []

		while  self.current_char != None:
			# Check for space & tab
			if self.current_char in ' \t':
				self.advance()

			elif self.current_char == '#':
				self.skip_comment()

			elif self.current_char in ';\n':
				tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
				self.advance()

			#######################
			# Check for digits
			elif self.current_char in DIGITS:
				tokens.append(self.make_number())

			#######################
			# Check for var assignments

			elif self.current_char in LETTERS:
				tokens.append(self.make_identifier())

			#######################
			# Check for stuff

			elif self.current_char == '"':
				tokens.append(self.make_string())

			elif self.current_char == '+':
				tokens.append(Token(TT_PLUS, pos_start=self.pos))
				self.advance()

			elif self.current_char == '-':
				tokens.append(Token(TT_MINUS, pos_start=self.pos))
				self.advance()

			elif self.current_char == '*':
				tokens.append(self.make_power_of())
				self.advance()

			elif self.current_char == '/':
				tokens.append(Token(TT_DIV, pos_start=self.pos))
				self.advance()

			elif self.current_char == '^':
				tokens.append(Token(TT_POWER, pos_start=self.pos))
				self.advance()

			elif self.current_char == '%':
				tokens.append(Token(TT_MOD, pos_start=self.pos))
				self.advance()

			elif self.current_char == '=':
				tokens.append(self.make_equals())

			elif self.current_char == '<':
				tokens.append(self.make_less_than())

			elif self.current_char == '>':
				tokens.append(self.make_greater_than())

			elif self.current_char == '!':
				tok, error = self.make_not_equals()
				if error: return [], error
				tokens.append(tok)

			elif self.current_char == ',':
				tokens.append(Token(TT_COMMA, pos_start=self.pos))
				self.advance()

			#######################
			# Check for parentheses
			elif self.current_char == '(':
				tokens.append(Token(TT_LPAREN, pos_start=self.pos))
				self.advance()

			elif self.current_char == ')':
				tokens.append(Token(TT_RPAREN, pos_start=self.pos))
				self.advance()

			elif self.current_char == '[':
				tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
				self.advance()

			elif self.current_char == ']':
				tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
				self.advance()

			elif self.current_char == '{':
				tokens.append(Token(TT_LCURLY, pos_start=self.pos))
				self.advance()
			elif self.current_char == '}':
				tokens.append(Token(TT_RCURLY, pos_start=self.pos))
				self.advance()

			#######################
			else: # Check for errors
				pos_start = self.pos.copy()
				char = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.pos,"'" + char + "'")

		tokens.append(Token(TT_EOF, pos_start=self.pos))
		return tokens, None

	def make_number(self):
		num_str = ''
		dot_count = 0
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1
				num_str += '.'
			else:
				num_str += self.current_char
			self.advance()

		if dot_count == 0:
			return Token(TT_INT, int(num_str), pos_start, self.pos)
		else:
			return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

	def make_string(self):
		string = ''
		pos_start = self.pos.copy()
		escape_character = False
		self.advance()

		escape_characters = {
			'n': '\n',
			't': '\t'
		}

		while self.current_char != None and (self.current_char != '"' or escape_character):
			if escape_character:
				string += escape_characters.get(self.current_char, self.current_char)
			else:
				if self.current_char == "\\":
					escape_character = True
				else:
					string += self.current_char
			self.advance()
			escape_character = False

		self.advance()
		return Token(TT_STRING, string, pos_start, self.pos)

	def make_identifier(self):
		id_str = ''
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
			id_str += self.current_char
			self.advance()

		tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
		return Token(tok_type, id_str, pos_start, self.pos)

	def make_not_equals(self):
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

		self.advance()
		return None, ExpectedCharError(pos_start, pos_end, "'=' after '!'")

	def make_equals(self):
		tok_type = TT_EQUALS
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_EE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_less_than(self):
		tok_type = TT_LT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_LTE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_greater_than(self):
		tok_type = TT_GT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TT_GTE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_power_of(self):
		tok_type = TT_MUL
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '*':
			self.advance()
			tok_type = TT_POWER

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def skip_comment(self):
		self.advance()

		while self.current_char != '\n':
			self.advance()

		self.advance()

if __name__ == '__main__':
	lexer = Lexer("test", "#Comment\n")
	print(lexer.make_tokens())