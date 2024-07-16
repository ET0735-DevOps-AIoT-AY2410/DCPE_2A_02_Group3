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

        uid = A[0]
        #convert output to list
        A_list = A[1].split(', ')
        print(A_list)
        #convert to list of strings
        card_data = [int(i) for i in A_list]

        print("uid of card:",uid)
        print("data stored on card:", card_data) 


def Write_data_to_rfid():
      reader.write('500 , 5352631234567890')



if __name__ == "__main__":
    reader = rfid_reader.init()
    read_rfid_info()
   
