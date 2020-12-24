# from this video: https://www.youtube.com/watch?v=51f3ZazNW-w
import RPi.GPIO as GPIO
import time

channel = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

def motor_on(pin):
	GPIO.output(pin, GPIO.LOW)

def motor_off(pin):
	GPIO.output(pin, GPIO.HIGH)

if __name__ == '__main__':
	try:
		motor_on(channel)
		time.sleep(3)
		motor_off(channel)
		time.sleep(1)
		GPIO.cleanup()
	except KeyboardInterrupt:
		GPIO.cleanup()
		pass
