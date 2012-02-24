#! /usr/bin/python
# tape.py - classes to visually display tape(s) on the terminal

import os, sys, time

class TapeError(Exception): pass

rows, columns = os.popen('stty size', 'r').read().split()

class Tapes(object):
	"""Display multiple tapes without having them blitz each other!
	Also allow text buffer!"""
	
	def __init__(self, tapes):
		"""Create a number of simultaneously displayed Tapes with the given contents"""
		self.tapes = tapes
		self.text_buffer = ""
		
		self._render_tapes()
		
	def move_left(self, tape):
		"""Move the pointer on the given tape one step to the left"""
		self.tapes[tape].move_left(render=False)
		self._render_tapes()
		
	def move_right(self, tape):
		"""Move the pointer on the given tape one step to the right"""
		self.tapes[tape].move_right(render=False)
		self._render_tapes()
		
	def update(self, tape, n):
		"""Update the value at the current position of the tape"""
		self.tapes[tape].update(n, render=False)
		self._render_tapes()
		
	def get(self, tape):
		"""Get the value at the current position of the given tape"""
		return self.tapes[tape].get()
		
	def putc(self, c):
		"""Print a character to the text buffer"""
		self.text_buffer += c
		self._render_tapes()
		
	def _render_tapes(self):
		self._reset_screen()
		for tape in self.tapes:
			tape._render(reset=False)
		print
		print self.text_buffer
			
	def _reset_screen(self):
		print "\x1b[2J\x1b[H" # clear the terminal
		

class Tape(object):
	"""Represents a tape to be printed to the screeen"""
	
	def __init__(self, contents, cell_width=3, default=0, right_infinite=True, 
	             left_infinite=False):
		
		self.contents = contents
		self.pos = 0
		self.default = default
		self.cell_width = cell_width
		self.right_infinite = right_infinite
		self.left_infinite = left_infinite
		
		self._render()
		
	def move_left(self, render=True):
		"""Move the tape one position to the left"""
		if (self.pos == 0 and not self.left_infinite):
			raise TapeError, "tape bounds exceeded to the left"
		self.pos -= 1
		if render: self._render()
		
	def move_right(self, render=True):
		"""Move the tape one position to the left"""
		if (self.pos == len(self.contents)-1 and not self.right_infinite):
			raise TapeError, "tape bounds exceeded to the right"
		self.pos += 1
		if render: self._render()
		
	def update(self, n, render=True):
		"""Update the value at the current position of the tape"""
		self.contents[self.pos] = n
		if render: self._render()
		
	def get(self):
		return self.contents[self.pos]
		
	def _render(self, reset=True):
		if reset: self._reset_screen()
		rows, columns = os.popen('stty size', 'r').read().split()
		columns = int(columns)
		
		full_width = self.cell_width + 3 # plus padding
		cells = columns / full_width
		centre_cell = cells / 2 + 1
		base = self.pos - (cells - centre_cell + 1)
		
		arrow_pos = (centre_cell * (full_width) + (full_width / 2))
		print arrow_pos * " " + "|"
		print arrow_pos * " " + "V"
		for i in xrange(
		print "-" * columns
		
		for i in xrange(cells):
			sys.stdout.write("| ")
			if ((not self.left_infinite) and (i + base < 0)) or \
			   ((not self.right_infinite) and (i + base >= len(self.contents))):
				sys.stdout.write(" " * self.cell_width)
			else:
				while i + base >= len(self.contents):
					self.contents.append(self.default)
				sys.stdout.write(str(self.contents[i + base]).center(self.cell_width))
			sys.stdout.write(" ")
			
		sys.stdout.write("\n")
		print "-" * columns
		
	def _reset_screen(self):
		print "\x1b[2J\x1b[H" # clear the terminal
			
		
		
		
if __name__ == "__main__":
	contents = [1, 2, 3, 4, 5, 6]
	ts = Tapes((contents, contents))
	ts.move_right(0)
	time.sleep(0.5)
	ts.move_right(1)
	time.sleep(0.5)
	ts.update(0, 78)
	ts.move_right(1)
	time.sleep(0.5)
	ts.move_right(0)
	time.sleep(0.5)
	ts.move_right(0)
	time.sleep(0.5)
#---------------------------
 #| 012 | 070 | 000 | 000|  
#---------------------------	
		
		
#"""


#"""
	