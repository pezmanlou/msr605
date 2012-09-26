import libMSR605


reader = libMSR605.msr605('/dev/ttyUSB0')

#print "setting 5 5 5 bpc"
#reader.setBitsPerCharacter([5,5,5])

print "Firmware Version: " + reader.getFirmwareVersion()
print "Device Model: " + reader.getDeviceModel()


print "Write something"
reader.writeIsoHiCo(['xxx  ','580','009'])
print reader.readIso()
#print "RAWW Read, Baby!"
#a = reader.readRaw();
#print a
#print [len(a[0]), len(a[1]), len(a[2])]
#print reader.readIso()
#print "Erasing..."
#reader.eraseCard(True, True, True)
#print "Reading..."
#print reader.readIso()

#print reader.readIso()

# woo card copying works!
#reader.writeIsoHiCo(reader.readIso())

#print reader.readIso()
reader.close()
