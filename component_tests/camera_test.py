from PIL import Image
from picamera import PiCamera
from time import sleep
import os

def take_photo():
	i = 0

	while os.path.exists("test%s.jpg" % i):
		i += 1
	
	camera = PiCamera()
	camera.start_preview()

	sleep(2)

	camera.capture('./test%s.jpg' % i)
	camera.stop_preview()
	print("Image {} taken...".format(i))

	img = Image.open('./test%s.jpg' % i)
	img = img.rotate(180)
	img.save("./test%s.jpg" % i)
	img.close()
	print("Image {} saved".format(i))

