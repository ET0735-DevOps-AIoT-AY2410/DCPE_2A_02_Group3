import RPi.GPIO as GPIO
import signal
from hal import hal_rfid_reader as rfid_reader
import time


def read_uid():
    for i in range(5):
        if i == 5:
            break
        print ("executing")
        rfid_reader.SimpleMFRC522.read_id_no_block()
        time.sleep(5)
        
if __name__ == "__main__":
    read_uid()