"""
Listen to serial, return most recent numeric values
Lots of help from here:
http://stackoverflow.com/questions/1093598/pyserial-how-to-read-last-line-sent-from-serial-device
"""
from threading import Thread
import time
import serial
import datetime
import logging
import os.path
import os

last_received = ''
def receiving(ser):
    global last_received
    buffer = ''
    while True:
        if '\n' in buffer:
            last_received, buffer = buffer.split('\n')[-2:]
        else:
            buffer += ser.read(1)  # this will block until one more char or timeout
        buffer += ser.read(ser.inWaiting()) # get remaining buffered chars


class SerialData(object):
    def __init__(self, port="/dev/ttyACM0", baudrate=9600, init=50):
        try:
            self.ser = ser = serial.Serial(
                port,
                baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
                xonxoff=0,
                rtscts=0,
                interCharTimeout=None
                )
        except serial.serialutil.SerialException:
            #no serial connection
            logging.warning('not possible to establish connection with '+port)
            self.ser = None
        else:
#            logging.info('Starting connection with '+port)
            Thread(target=receiving, args=(self.ser,)).start()

    def next(self):
        global last_received
        if self.ser == None:
            return -9999 #return anything so we can test when Arduino isn't connected
        #return a float value or try a few times until we get one
        while True:
            raw_line = last_received
            if raw_line == '':
                time.sleep(.01)
                continue
            try:
                last_received=''
                return raw_line.strip()
            except ValueError:
                continue
        return 0.

    def __del__(self):
        if self.ser:
            self.ser.close()
            


if __name__=='__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d","--dev")
    parser.add_option("-l","--log")
    (options,args)=parser.parse_args()

    port=options.dev
    #logging.basicConfig(format='%(asctime)s,%(message)s', datefmt='%Y-%m-%d %H:%M:%S',filename=options.log,level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s,%(message)s', datefmt='%s',filename=options.log,level=logging.DEBUG)
    s = SerialData(port)
    while True:

#        if (os.path.isfile(options.log)==False):
#            os.system("touch "+options.log)
            
        data=s.next()
        logging.info(data)
        if data==-9999:
            print 'no connection with '+port+". Quit"
            exit(-1)

