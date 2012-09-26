import libMSR605


reader = libMSR605.msr605('/dev/ttyUSB0')
print reader.readIso()




reader.close()



#while True:
# print "> " + read_until(ESC)




#//led off
#1B 81


#def get_device_model():
#  1B 74



