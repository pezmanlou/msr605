import serial
import binascii

ESC = '\x1b'
RESET = '\x1b\x61'
READ_ISO = '\x1b\x72'
WRITE_ISO = '\x1b\x77'
COMMUNICATIONS_TEST = '\x1b\x65'
ALL_LED_OFF = '\x1B\x81'
ALL_LED_ON = '\x1B\x82'
GREEN_LED_ON = '\x1B\x83'
YELLOW_LED_ON = '\x1B\x84'
RED_LED_ON = '\x1B\x85'
SENSOR_TEST = '\x1B\x86'
RAM_TEST = '\x1B\x87'


def read_until(byte):
  b = ""
  d = ""
  while True:
    b = s.read()
    if (b == byte):
      return d
    d += binascii.unhexlify(binascii.hexlify(b))

serial_port = '/dev/ttyUSB0'

s = serial.Serial(serial_port, 9600)
s.write(RESET)
s.write(READ_ISO)

read_until(ESC)
read_until('\x73')
read_until(ESC)
s.read()
print "t1: " + read_until(ESC)
s.read()
print "t2: " + read_until(ESC)
s.read()
print "t3: " + read_until('\x1c')
read_until(ESC)
print "status: " + binascii.hexlify(s.read())

#while True:
# print "> " + read_until(ESC)


s.close

#//led off
#1B 81


#def get_device_model():
#  1B 74



