from copy import copy
import csv
import curses
from curses import wrapper
import time
from datetime import datetime
from soil_sensor import *

# initialize the curses screen
stdscr = curses.initscr()
bar = "|"
		
def get_file_lines(filename="soil_data.txt"):
	with open(filename, 'r') as the_file:
		file_lines = the_file.readlines()
	the_file.close()
	return len(file_lines)

def load_soil_data(n=7): # returns n days worth of data 
	with open('soil_data.txt', 'r') as soil_data:
		soil_lines = soil_data.readlines()
	soil_data.close()
	
	last_n = []
	i = 1
	num_lines = len(soil_lines)
	while (i <= n) and (i < num_lines):
		last_n.insert(0,soil_lines[num_lines-i].split(','))
		i += 1

	return last_n, (len(last_n))

def draw_sensor_win(window, dates, data, number=0):
	window.addstr(1,1, "Soil Sensor " + str(number) + ":", curses.A_BOLD)

	window.addstr(6,1,"Curr. Val.:")
	window.addstr(7,1, str(round(get_sensor_data(number),4)) + "V")

	# x-axis date labels
	date_min = dates[0]
	date_max = dates[len(dates)-1]
	window.addstr(11,13,date_min, curses.color_pair(1))
	window.addstr(11,43,date_max, curses.color_pair(1))

	# y-axis voltage labels (change to some scale of wet/dry? V is cryptic)
	window.addstr(1,48,"{:.2f}".format(max(data)) + "V")
	window.addstr(8,48,"{:.2f}".format(min(data)) + "V")
	
	graph = window.derwin(10, 32, 1, 15)
	draw_graph(graph, dates, data)
	window.border(0)
	pass
	
def draw_graph(window, dates, data):
	# data => y range 0-8
	#Result = ((Input - InputLow) / (InputHigh - InputLow)) * (outputHigh - OutputLow) + OutputLow  
	min_input = min(data)
	max_input = max(data)
	scaled_data = []
	for val in data:
		val_scaled = ((val - min_input) / (max_input - min_input)) * (7 - 0) + 0
		scaled_data.append(int(val_scaled))
	i = 0
	while i < len(scaled_data):
		window.addstr(8-scaled_data[i],i+1,"¤",curses.color_pair(2) )
		i += 1
	window.border(0)
	pass
	
def main(stdscr):
	height, width = stdscr.getmaxyx() # get the window size
	curses.start_color()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
	 
	# header
	stdscr.addstr(1,1, " " * (width-2), curses.color_pair(1) )
	stdscr.addstr(1,1, "Plant Monitor",curses.color_pair(1) )
	stdscr.hline(2,1,"_",width)

	# footer
	stdscr.addstr(height -1,1, " " * (width -2),curses.color_pair(1) )
	stdscr.addstr(height -1,1, "Hit q to quit",curses.color_pair(1) )
	 
	prev_ch0, prev_ch1, prev_ch2, prev_ch3 = get_all_data()

	# load in soil data
	last_n, days_old = load_soil_data(30)
	dates = []
	times = []
	s0_data = []
	s1_data = []
	s2_data = []
	s3_data = []

	# split out soil data
	for line in last_n:
		dates.append(line[0])
		times.append(line[1])
		s0_data.append(float(line[2]))
		s1_data.append(float(line[3]))
		s2_data.append(float(line[4]))
		s3_data.append(float(line[5]))
	# remove this print statement later:
	stdscr.addstr(height-3,1,str(days_old))

	# gregarious monstera ascii art
	with open('med_monstera.txt', 'r') as leaves:
		leaf_array = leaves.read().split('\n')
		i = height - len(leaf_array)
		for row in leaf_array:	
			stdscr.addstr(i, width - 50, row)
			i += 1		
	leaves.close()

	# Define windows to be used for bar charts
	# curses.newwin(height, width, begin_y, begin_x)
	win0 = curses.newwin(13, 54, 3, 1)
	win1 = curses.newwin(13, 54, 17, 1) 
	win2 = curses.newwin(13, 54, 31, 1)
	win3 = curses.newwin(13, 54, 3, 56)

	k = 0
	written_today = False
	while True:
		if k != ord('q'):
			# read data values
			ch0_voltage, ch1_voltage, ch2_voltage, ch3_voltage = get_all_data()

			# these will hopefully cutdown on times that we render the graphs
			if prev_ch0 != ch0_voltage:
				prev_ch0 = ch0_voltage
				win0.clear()

			if prev_ch1 != ch1_voltage:

				prev_ch1 = ch1_voltage
				win1.clear()

			if prev_ch2 != ch2_voltage:
				prev_ch2 = ch2_voltage
				win2.clear()

			if prev_ch3 != ch3_voltage:
				prev_ch3 = ch3_voltage
				win3.clear()

			now = datetime.now()
			stdscr.addstr(1,width-10,now.strftime("%x"), curses.color_pair(1))
			# write to csv once a day
			# not sure the logic for this checks out...
			if len(last_n) != 0:
				if last_n[len(last_n)-1][0] != now.strftime("%x") and written_today == False:
					with open('soil_data.txt', 'a') as soil_data:
							soil_data.write(now.strftime("%x") + ',' 
								+ now.strftime("%X") + ','
								+ str(ch0_voltage) + ',' + str(ch1_voltage) + ',' 
								+ str(ch2_voltage) + ',' + str(ch3_voltage) + "\n")
					written_today = True
					soil_data.close()

			#draw_sensor_win(window, dates, data, number=0):
			draw_sensor_win(win0, dates, s0_data, 0)
			draw_sensor_win(win1, dates, s1_data, 1)
			draw_sensor_win(win2, dates, s2_data, 2)
			draw_sensor_win(win3, dates, s3_data, 3)

			# refresh windows
			win0.refresh()
			win1.refresh()
			win2.refresh()
			win3.refresh()
			
			#stdscr.refresh()
			time.sleep(1)
			stdscr.nodelay(1)
			k = stdscr.getch() # look for a keyboard input, but don't wait
		elif k == ord('q'):
			break

wrapper(main)
curses.endwin() # restore the terminal settings back to the original

