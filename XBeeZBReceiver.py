
from xbee import ZigBee
import serial
import struct

# TODO Replace with the serial port where your receiver module is connected.
PORT = '/dev/ttyAMA0'
# TODO Replace with the baud rate of you receiver module.
BAUD_RATE = 9600

# Open serial port
myDevice = serial.Serial(PORT, BAUD_RATE)

# Create API object
xbee = ZigBee(myDevice)

def prettyHexString(str):
    "split string by 2 length"
    return ' '.join([str[i:i+2] for i in range(0, len(str), 2)])

# Continuously read and print packets
print(">> Waiting for data...")
while True:
    try:
        response = xbee.wait_read_frame()
        source_addr = response['source_addr_long'].hex().upper()
        payload = prettyHexString(response['rf_data'].hex().upper())
        data = struct.unpack('ff', response['rf_data'])
        print('From %s >> [%s] | { temperature: %.1f degrees, humidity: %.1f%% }' % (source_addr, payload, data[0], data[1]))

    except KeyboardInterrupt:
        break

myDevice.close()
