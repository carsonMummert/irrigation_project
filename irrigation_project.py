from copy import copy
import csv
import curses
from curses import wrapper
import time
from datetime import datetime
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# setup of mcp3008 adc, supports up to 8 sensors
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)
chan3 = AnalogIn(mcp, MCP.P3)

bar = '█' # an extended ASCII 'fill' character
stdscr = curses.initscr() # create curses screen

# records soil values, which are being read continuously 
def get_sensor_data():
	ch0 = chan0.voltage
	ch1 = chan1.voltage
	ch2 = chan2.voltage
	ch3 = chan3.voltage
	return ch0, ch1, ch2, ch3

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
	 
	prev_ch0, prev_ch1, prev_ch2, prev_ch3 = get_sensor_data()

	# previous soil data loaded here
	last_n, days_old = load_soil_data()
	dates = []
	times = []
	s1_data = []
	s2_data = []
	s3_data = []
	s4_data = []

	for line in last_n:
		dates.append(line[0])
		times.append(line[1])
		s1_data.append(line[2])
		s2_data.append(line[3])
		s3_data.append(line[4])
		s4_data.append(line[5])
	# stdscr.addstr(height-3,1,s1_data[0])

	# stdscr.addstr(height-3,1,last_n[len(last_n)-1][0])
	# stdscr.addstr(height-4,1,str(days_old))
	stdscr.addstr(height-20,1,str(days_old))

	# gregarious monstera ascii art
	with open('med_monstera.txt', 'r') as leaves:
		leaf_array = leaves.read().split('\n')
		i = height - len(leaf_array)
		for row in leaf_array:	
			stdscr.addstr(i, width - 50, row)
			i += 1		
	leaves.close()

	# labels
	stdscr.addstr(4,1, "Soil Sensor 0:")
	stdscr.addstr(16,1, "Soil Sensor 1:")
	stdscr.addstr(20,1, "Soil Sensor 2:")
	stdscr.addstr(24,1, "Soil Sensor 3:")

	 
	# Define windows to be used for bar charts
	# curses.newwin(height, width, begin_y, begin_x)
	win1 = curses.newwin(10, 32, 3, 15) 
	win2 = curses.newwin(3, 32, 15, 15)
	win3 = curses.newwin(3, 32, 19, 15)
	win4 = curses.newwin(3, 32, 23, 15)

	# Use the 'q' key to quit
	k = 0
	written_to = False
	while (k != ord('q')):
		ch0_voltage, ch1_voltage, ch2_voltage, ch3_voltage = get_sensor_data() # get the data values
		# these will hopefully cutdown on times that we render the graphs
		if prev_ch0 != ch0_voltage:
			prev_ch0 = ch0_voltage
			win1.clear()

		if prev_ch1 != ch1_voltage:

			prev_ch1 = ch1_voltage
			win2.clear()

		if prev_ch2 != ch2_voltage:
			prev_ch2 = ch2_voltage
			win3.clear()

		if prev_ch3 != ch3_voltage:
			prev_ch3 = ch3_voltage
			win4.clear()

		now = datetime.now()
		stdscr.addstr(1,width-10,now.strftime("%x"), curses.color_pair(1))
		# write to csv once a day
		# not sure the logic for this checks out...
		# the written_to bool counts 
		if len(last_n) != 0 and written_to == False:
			if last_n[len(last_n)-1][0] != now.strftime("%x"):
				with open('soil_data.txt', 'a') as soil_data:
						soil_data.write(now.strftime("%x") + ',' 
							+ now.strftime("%X") + ','
							+ str(ch0_voltage) + ',' + str(ch1_voltage) + ',' 
							+ str(ch2_voltage) + ',' + str(ch3_voltage) + "\n")
				soil_data.close()
				written_to = True

		win1.border(0)
		win2.border(0)
		win3.border(0)
		win4.border(0)
		
		date_min = dates[0]
		date_max = dates[len(dates)-1]
		stdscr.addstr(13,13,date_min, curses.color_pair(1))
		stdscr.addstr(13,43,date_max, curses.color_pair(1))
		
		stdscr.addstr(4,48,max(s1_data)[0:5] + "V")
		stdscr.addstr(11,48,min(s1_data)[0:5] + "V")

		ch0_scaled = ((ch0_voltage - 0) / (4 - 0)) * (30 - 0) + 0
		ch1_scaled = ((ch1_voltage - 0) / (4 - 0)) * (30 - 0) + 0
		ch2_scaled = ((ch2_voltage - 0) / (4 - 0)) * (30 - 0) + 0
		ch3_scaled = ((ch3_voltage - 0) / (4 - 0)) * (30 - 0) + 0

		# create bars bases on the returned values
		win1.addstr(1, 1, bar * int(ch0_scaled), curses.color_pair(2))
		win1.refresh()
		win2.addstr(1, 1, bar * int(ch1_scaled), curses.color_pair(3))
		win2.refresh()
		win3.addstr(1, 1, bar * int(ch2_scaled), curses.color_pair(2))
		win3.refresh()
		win4.addstr(1, 1, bar * int(ch3_scaled), curses.color_pair(3))
		win4.refresh()
		
		# add numeric values beside the bars (we get 16 places of precision, but round
		# em off to be pretty
		stdscr.addstr(8,1,"Curr. Val.:")
		stdscr.addstr(9,1, str(round(ch0_voltage,4)) + "V ",curses.A_BOLD )
		stdscr.addstr(15,50, str(round(ch1_voltage,4)) + "V ",curses.A_BOLD )
		stdscr.addstr(19,50, str(round(ch2_voltage,4)) + "V ",curses.A_BOLD )
		stdscr.addstr(23,50, str(round(ch3_voltage,4)) + "V ",curses.A_BOLD )
		stdscr.refresh()
		time.sleep(1)
		stdscr.nodelay(1)
		k = stdscr.getch() # look for a keyboard input, but don't wait

wrapper(main)
curses.endwin() # restore the terminal settings back to the original

