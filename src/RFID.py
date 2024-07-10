import RPi.GPIO as GPIO
import signal
from hal import hal_rfid_reader as rfid_reader
import time
import sys


def read_rfid_info():
        #redirect output to prevent read() funtion from printing
        ignore_stdout = sys.stdout
        sys.stdout = open('trash', 'w')

        A = reader.read()
        #redirect output back to normal
        sys.stdout.close()
        sys.stdout = ignore_stdout
        
        print(" uid of card:",A[0])
        # use repr as null characters unprintable , can remove if info is there?
        print("data stored on card:",repr(A[1])) 
        
if __name__ == "__main__":
    reader = rfid_reader.init()
    read_rfid_info()