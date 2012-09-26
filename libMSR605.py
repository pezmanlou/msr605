# libMSR605.py
# written by Louis Bodnar
# end of september 2012

import serial
import binascii
import time




ESC = '\x1B'
FS = '\x1C'
ACK = '\x1B\x79'

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
    # open port
    self.__s = serial.Serial(port, 9600)

    # initialize (btw the programming manual has some of this stuff backwards)
    self.__s.write(RESET)
    self.__s.write(COMMUNICATIONS_TEST)

    if (self.__s.read() != ESC):
      print "could not init"

    if (self.__s.read() != 'y'):
      print "could not init"

    self.__s.write(RESET)


  def readIso(self):
    self.__s.write(RESET)
    self.__s.write(READ_ISO)
    data = ['','','']
    status = '\x00'


    # read <esc>s<esc>

    if (self.__s.read() != ESC):
      print "expected byte mismatch"
      return data


    if (self.__s.read() != 's'):
      print "expected byte mismatch"
      return data

    if (self.__s.read() != ESC):
      print "expected byte mismatch"
      return data




    # next byte should be '\x01'
    if (self.__s.read() == '\x01'):
      data[0] = self.read_until(ESC)
    else:
      print "expected byte mismatch"
      return data

    # next byte should be '\x02'
    if (self.__s.read() == '\x02'):
      data[1] = self.read_until(ESC)
    else:
      print "expected byte mismatch"
      return data

    # next byte should be '\x03'
    if (self.__s.read() == '\x03'):
      data[2] = self.read_until(FS)
    else:
      print "expected byte mismatch"
      return data

    if (self.__s.read() != ESC):
      print "expected byte mismatch"
      return data

    # check status
    if (self.__s.read() != '\x30'):
      print "got bad status, something bad may have happened"
      return data

    return data







  def __setHiCo(self):
    self.__s.write('\x1B\x78')
    if (self.__s.read() != ESC):
      print "expected byte mismatch"

    # check status
    if (self.__s.read() != '0'):
      print "expected byte mismatch"






  def __setLowCo(self):
    self.__s.write('\x1B\x79')
    if (self.__s.read() != ESC):
      print "expected byte mismatch"

    # check status
    if (self.__s.read() != '0'):
      print "expected byte mismatch"




  def writeIsoHiCo(self, data):
    self.__setHiCo()
    self.__writeIso(data)


  def writeIsoLowCo(self, data):
    self.__setLowCo()
    self.__writeIso(data)



  def __writeIso(self, data): # TODO: add check for non-iso chars

    # for whatever reason, it seems that the last char of the third track must be a ? or it wont go in to write mode
    if (data[2][-1:] != '?'):
      print "last char of track 3 not '?', fixing."
      data[2] += '?'

    # another quirk - the msr605 appends a % to the beginning of track one, so if you already have one, this deletes it (that way you wont end up with a bunch of duplicate % signs)
    if (data[0][0] == '%'):
      data[0] = data[0][1:]
      
    command = ''
    command += ESC
    command += '\x77'
    command += ESC
    command += '\x73'
    command += ESC
    command += '\x01'
    command += data[0]
    command += ESC
    command += '\x02'
    command += data[1]
    command += ESC
    command += '\x03'
    command += data[2]
    command += FS

    self.__s.write(command)

    if (self.__s.read() != ESC):
      print "expected byte mismatch"

    # check status
    if (self.__s.read() != '\x30'):
      print "got bad status, something bad may have happened"


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

  def setBitsPerCharacter(self, bpc): # broken (I send the correct bits, it just wont give me the expected response)
    if (bpc[0] < 5 or bpc[0] > 8):
      print "track 1 bits wrong size (can be between 5 and 8 bits per character)"
      return 0
    if (bpc[1] < 5 or bpc[1] > 8):
      print "track 2 bits wrong size (can be between 5 and 8 bits per character)"
      return 0
    if (bpc[2] < 5 or bpc[2] > 8):
      print "track 3 bits wrong size (can be between 5 and 8 bits per character)"
      return 0


    command = ""
    command += ESC
    command += '\x6F'
    command += ESC
    command += '\x08' #str(bpc[0])
    command += '\x08' #str(bpc[1])
    command += '\x08' #str(bpc[2])
    print "Command: " + command


    self.__printHexToDebug(command)
    self.__s.write(command)

    self.__read(ESC)
    self.__read('\x41')
    self.__read('\x08')
    self.__read(bpc[1])
    self.__read(bpc[2])


  def __read(self, byte):
    a = self.__s.read()
    if (a != byte):
      print "Expected [" + binascii.hexlify(byte) + "] got [" + binascii.hexlify(a) + "]"
      return 0
    #print "got: " + "[" + binascii.hexlify(a) + "]"
    return 1

  def __printHexToDebug(self, toPrint):
    hexd = ""
    for a in toPrint:
      hexd += "[" + binascii.hexlify(a) + "]"
    print hexd



  def getFirmwareVersion(self):
    command = ""
    command += ESC
    command += '\x76'

    self.__s.write(command)

    self.__read(ESC)

    time.sleep(.1)

    version = ""
    while (self.__s.inWaiting()):
      version += self.__s.read()

    return version



  def getDeviceModel(self):
    command = ""
    command += ESC
    command += '\x74'


    self.__s.write(command)

    self.__read(ESC)

    time.sleep(.1)

    version = ""
    while (self.__s.inWaiting()):
      version += self.__s.read()

    if (version[-1:] != 'S'):
      print "got back bad response"
      return 0

    return version[:-1]
     



  def eraseCard(self, trackOne, trackTwo, trackThree):

    command = ""
    command += ESC
    command += '\x63'

    if (trackOne and not trackTwo and not trackThree):
      command += '\x00'
    elif (not trackOne and trackTwo and not trackThree):
      command += '\x02'
    elif (not trackOne and not trackTwo and trackThree):
      command += '\x04'
    elif (trackOne and trackTwo and not trackThree):
      command += '\x03'
    elif (not trackOne and not trackTwo and trackThree):
      command += '\x05'
    elif (not trackOne and trackTwo and trackThree):
      command += '\x06'
    elif (trackOne and trackTwo and trackThree):
      command += '\x07'


    self.__printHexToDebug(command)    
    self.__s.write(command)
    self.__read(ESC)
    isOK = self.__s.read()


    if (isOK == '\x30'):
      return True

    return False


  def __whatsInMyBuffer(self):

    a = self.__s.read()
    time.sleep(.01)
    while (self.__s.inWaiting()):
      a += self.__s.read()
      time.sleep(.01)
    self.__printHexToDebug(a)
    return




  def readRaw(self):
    command = ""
    command += ESC
    command += '\x6D'
    self.__s.write(command)


    self.__read(ESC)
    self.__read('\x73')


    self.__read(ESC)
    self.__read('\x01')
    length = int(binascii.hexlify(self.__s.read()), 16)
    trackOne = []
    while (length > 0):
      length -= 1
      trackOne.append(self.__s.read())


    self.__read(ESC)
    self.__read('\x02')
    length = int(binascii.hexlify(self.__s.read()), 16)
    trackTwo = []
    while (length > 0):
      length -= 1
      trackTwo.append(self.__s.read())


    self.__read(ESC)
    self.__read('\x03')
    length = int(binascii.hexlify(self.__s.read()), 16)
    trackThree = []
    while (length > 0):
      length -= 1
      trackThree.append(self.__s.read())

    return ["".join(trackOne), "".join(trackTwo), "".join(trackThree)]








































