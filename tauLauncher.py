import time, omega
from os import system, name
def run(title, code):
	if name == 'nt':
		system('cls')
	else:
		system('clear')
	# The st and et are here to calculate how much time an operation takes
	st = time.time()
	result, error = omega.run(title, code)
	et = time.time()

	if error: res = error.as_string()
	elif result: res = repr(result)

	if res != "[None]":
		print("\n\n" + res + "\n\n[Finished in " + str(st-et) + "s]\n\n" + "Do not close this window")