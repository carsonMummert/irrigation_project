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

# records soil values, which are being read continuously 
def get_sensor_data():
	ch0 = chan0.voltage
	ch1 = chan1.voltage
	ch2 = chan2.voltage
	ch3 = chan3.voltage
	return ch0, ch1, ch2, ch3
