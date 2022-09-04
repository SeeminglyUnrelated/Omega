import omega, time, sys
from platform import system, release, processor

# The st and et are here to calculate how much time an operation takes
try:
	with open(sys.argv[1]) as f:
		code = f.read()
	st = time.time()
	result, error = omega.run(sys.argv[1], code)
	et = time.time()

	if error: print(error.as_string())
	elif result: print(repr(result))
	input("Press Enter to exit")
except IndexError:
	print("| {Omega 1.0.0} \n| On:  " + 
	system() + " " + # Display OS
	release() + #  Display Version
	"  (" + processor() + ")" + # Display Processor
	" \n\n| Type \"exit()\" to exit shell\n"
	)

	while True:
		text = input('Omega > ') + "\n"
		if text.strip() == "": continue
		if text == "exit()": break
		elif text == "thicc" or text == "omega": 
			print("Is it just me, or is Omega looking kinda THICC")
			continue
		elif text == "shock arrow":
			print("         ____\n|) --->> code\n         ####")
			continue

		result, error = omega.run('<cIn>', text)

		if error: print(error.as_string())
		elif result:
			if repr(result) != "[None]":
				if len(result.elements) == 1:
					print(repr(result.elements[0]))
				else:
					print(repr(result))

print ("bye bye!!!!")
time.sleep(0.5)