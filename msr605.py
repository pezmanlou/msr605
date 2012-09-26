import serial

serial_port = '/dev/ttyUSB0'

s = serial.Serial(serial_port, 9600)
s.write('\x1B\x74');

b = '0';
while True:
  b = s.read();
  print b;
  #if (b == '\x1B'):
  #  s.write('\x1B\x72');

s.close;

#//led off
#1B 81


#def get_device_model():
#  1B 74
