import dht11sensor, camera_test

if __name__ == '__main__':
	try:
		try:
			 data_file = open("irrigation_data.txt", "a+")
		except:
			 exit("Oops, couldn't find data file. Exiting program")
		camera_test.take_photo()		
		dht11sensor.press_to_record(data_file)

	except KeyboardInterrupt:
		print("\nClosing program...")
		data_file.close()
		GPIO.cleanup()
		exit("\nExiting program... goodbye!")
                                                                
