#!/usr/bin/python

# Modules
import random # used to change starting location
import curses # a nice TUI
import time # To limit the number of frames drawn per second

# Basic curses settings
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)

#variables
the_box = (
	['   ','   ','   ','   ','   ', '   ','   ','   ','   ','   ', '   ','   ','   ','   ','   '], 
	['   ','   ','   ','   ','   ', '   ','   ','   ','   ','   ', '   ','   ','   ','   ','   '], 
	['   ','   ','   ','   ','   ', '   ','   ','   ','   ','   ', '   ','   ','   ','   ','   '], 
	['   ','   ','   ','   ','   ', '   ','   ','   ','   ','   ', '   ','   ','   ','   ','   '], 
	['   ','   ','   ','   ','   ', '   ','   ','   ','   ','   ', '   ','   ','   ','   ','   '], 
	['   ','   ','   ','   ','   ', '   ','   ','   ','   ','   ', '   ','   ','   ','   ','   '], 
	['   ','   ','   ','   ','   ', '   ','   ','   ','   ','   ', '   ','   ','   ','   ','   '], 
	['   ','   ','   ','   ','   ', '   ','   ','   ','   ','   ', '   ','   ','   ','   ','   '], 
	['   ','   ','   ','   ','   ', '   ','   ','   ','   ','   ', '   ','   ','   ','   ','   '], 
	['   ','   ','   ','   ','   ', '   ','   ','   ','   ','   ', '   ','   ','   ','   ','   '])

up_vel = 1 # This determines the vertical direction: 1 = up, 0 = down
left_vel = 1 # This determines the horizontal direction: 1 = left, 0 = right
current = [0, random.randint(0,4)] # Random starting location based on box size
paddle = ['   ', '   ', '   ','   ','   ', '[/]', '[^]','[^]','[^]','[\]','   ','   ','   ','   ','   ']

# Function for printing the box dynamically.
# Prevents needing large amounts of space for building the new box frame
def print_box(a_box):
	# local variables for printing
	count = 0
	box_size = len(a_box)

	# dynamically increment the screen row for printing
	# dynamically increment the box array for printing
	# increase the count for each loop
	while count < box_size:
		output = '|'
		for space in a_box[count]:
			output += space
		
		output += '|'
		stdscr.addstr(count, 0, output)
		count += 1

	# refresh the screen with the updated information
	paddle_out = '|'
	for space in paddle:
		paddle_out += space
	paddle_out += '|'
	
	stdscr.addstr(10, 0, paddle_out)
	stdscr.refresh()

# Show the initial box with
print_box(the_box)

# Begin moving the numbers around
try:
	while(1):
		# Future should be reset each round
		future = [0, 0]

		# Adjust this time to effect the time between screen refreshes
		time.sleep(.1)
		
		# Reverse direction at the vertical boundaries
		if current[0] == 0 and up_vel == 1:
			up_vel = 0
		elif current[0] == 9 and up_vel == 0 and paddle[current[1]] != '   ':
			up_vel = 1
		elif current[0] == 9 and up_vel == 0 and paddle[current[1]] == '   ':
			break

		# Reverse direction at the horizontal boundaries		
		if current[1] == 0 and left_vel == 1:
			left_vel = 0
		elif current[1] == 14 and left_vel == 0:
			left_vel = 1
		
		# Update the vertical state	
		if up_vel == 1 and current[0] > 0:
			future[0] = current[0] - 1
		elif up_vel == 0 and current[0] < 9:
			future[0] = current[0] + 1
		elif current[0] == 0:
			future[0] = 1
		elif current[0] == 9:
			future[0] == 8		

		# Paddle redirection
		if current[0] == 9:
			if paddle[current[1]] == '[\\]' and paddle[current[1]] == '[/]':
				if left_vel == 1:
					left_vel = 0
				else:
					left_vel = 1

		# Update the horizontal state
		if left_vel == 1 and current[1] > 0:
			future[1] = current[1] - 1
		elif left_vel == 0 and current[1] < 14:
			future[1] = current[1] + 1
		elif current[1] == 0:
			future[1] = 1
		elif current[1] == 14:
			future[1] == 13		

		# Update the_box with the new co-ordinate
		the_box[future[0]][future[1]] = ' X '		
		the_box[current[0]][current[1]] = '   '		

		# Set current state to cacluted future state	
		current = future

		# print the box
		print_box(the_box)

		# Get user input

		input = stdscr.getch()

		stdscr.addstr(12, 0, str(input))
		stdscr.refresh()

		if input == 260 and paddle[0] == '   ':
			paddle.pop(0)
			paddle.append('   ')
		elif input  == 261 and paddle[14] == '   ':
			paddle.pop(14)
			paddle.insert(0, '   ')
		elif input == 113:
			break
except:
	pass


# End the program
curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()
