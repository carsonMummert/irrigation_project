# from this video: https://www.youtube.com/watch?v=51f3ZazNW-w
import RPi.GPIO as GPIO
import time

channel1  = 18
channel2 = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel1, GPIO.OUT)
GPIO.setup(channel2, GPIO.OUT)

def motor_on(pin):
	GPIO.output(pin, GPIO.LOW)

def motor_off(pin):
	GPIO.output(pin, GPIO.HIGH)

if __name__ == '__main__':
	try:
		print("Turning on Pump 1...")
		motor_on(channel1)
		time.sleep(1)
		motor_off(channel1)
		print("Done!")
		time.sleep(1)
		print("Turning on Pump 2...")
		motor_on(channel2)
		time.sleep(1)
		motor_off(channel2)
		print("Done!")
		time.sleep(1)
		GPIO.cleanup()
	except KeyboardInterrupt:
		GPIO.cleanup()
		pass
