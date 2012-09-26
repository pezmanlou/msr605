import serial






ESC = '\x1B'
FS = '\x1B'

RESET = '\x1B\x61'
READ_ISO = '\x1B\x72'
WRITE_ISO = '\x1B\x77'
COMMUNICATIONS_TEST = '\x1B\x65'
ALL_LED_OFF = '\x1B\x81'
ALL_LED_ON = '\x1B\x82'
GREEN_LED_ON = '\x1B\x83'
YELLOW_LED_ON = '\x1B\x84'
RED_LED_ON = '\x1B\x85'
SENSOR_TEST = '\x1B\x86'
RAM_TEST = '\x1B\x87'



class msr605:
  def __init__(self, port):
    self.__s = serial.Serial(port, 9600)
    self.__s.write(RESET)

  def readIso(self):
    self.__s.write(RESET)
    self.__s.write(READ_ISO)
    data = ['','','']
    status = '\x00'


    # read <esc>s<esc>

    if (self.__s.read() != ESC):
      print "something bad happened"
      return data


    if (self.__s.read() != 's'):
      print "something bad happened"
      return data

    if (self.__s.read() != ESC):
      print "something bad happened"
      return data




    # next byte should be '\x01'
    if (self.__s.read() == '\x01'):
      data[0] = self.read_until(ESC)
    else:
      print "something bad happened"
      return data

    # next byte should be '\x02'
    if (self.__s.read() == '\x02'):
      data[1] = self.read_until(ESC)
    else:
      print "something bad happened"
      return data

    # next byte should be '\x03'
    if (self.__s.read() == '\x03'):
      data[2] = self.read_until(FS)
    else:
      print "something bad happened"
      return data

    if (self.__s.read() != ESC):
      print "something bad happened"
      return data

    # check status
    if (self.__s.read() != '\x30'):
      print "something bad happened"
      return data

    return data





  def close(self):
    self.__s.close

  def read_until(self, byte):
    b = ""
    d = ""
    while True:
      b = self.__s.read()
      if (b == byte):
        return d
      d += b
