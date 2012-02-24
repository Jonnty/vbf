#! /usr/bin/python
# vbf.py - a tape-based visual brainfuck interpreter

import sys, time
from tape import Tape, Tapes, TapeError

f = open(sys.argv[1])

program = [c for c in f.read() if c in "<>,.-+[]"]
f.close()

prog_tape = Tape(program, right_infinite=False)
data_tape = Tape([0], 3)

tapes = Tapes((prog_tape, data_tape))

PROG = 0
DATA = 1
STEP_TIME = 0.2
SEEK_TIME = 0.05

while (1):
	time.sleep(STEP_TIME)
	c = prog_tape.get()
	
	if c == "<":
		tapes.move_left(DATA)
		print 1
	elif c == ">":
		tapes.move_right(DATA)
	elif c == ".":
		tapes.putc(chr(data_tape.get()))
	elif c == ",":
		tapes.update(DATA, ord(sys.stdin.read(1)))
		
	elif c == "+":
		tapes.update(DATA, (data_tape.get() + 1) % 256)
	elif c == "-":
		tapes.update(DATA, (data_tape.get() - 1) % 256)
	elif c == "[":
		if not data_tape.get():
			depth = 0
			while (prog_tape.get() != "]" or depth <= 0):
				if prog_tape.get() == "[":
					depth += 1
				elif prog_tape.get() == "]":
					depth -= 1
				time.sleep(SEEK_TIME)
				tapes.move_right(PROG)
	elif c == "]":
		if data_tape.get():
			depth = 0
			while (prog_tape.get() != "[" or depth > 0):
				tapes.move_left(PROG)
				if prog_tape.get() == "]":
					depth += 1
				elif prog_tape.get() == "[":
					depth -= 1
				time.sleep(SEEK_TIME)
	
	try:
		tapes.move_right(PROG)
	except TapeError:
		sys.exit(0) #terminated