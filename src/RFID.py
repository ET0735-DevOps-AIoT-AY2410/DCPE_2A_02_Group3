import RPi.GPIO as GPIO
import signal
import time
import sys
from hal import hal_rfid_reader as rfid_reader


def read_rfid_info(reader):
      #redirect output and read rfid
      ignore_stdout = sys.stdout
      sys.stdout = open('trash', 'w')
      A = reader.read()
      sys.stdout.close()
      sys.stdout = ignore_stdout

      #clean list
      A = [str(item) for item in A]
      cleaned_A = [item.strip(' ') for item in A]
      uid = cleaned_A[0]
      A_list = list(cleaned_A[1])
      A_list = ''.join(A_list)
      A_list = A_list.split(',')

      #convert into list of strings
      card_data = [int(i) for i in A_list]

      #print data
      print("uid of card:",uid)
      print("data stored on card:", card_data) 
      print(type(card_data[1]))

      return uid,card_data


def Write_data_to_rfid():

      reader.write('500,4465594948671029')



if __name__ == "__main__":
      reader = rfid_reader.init()
      read_rfid_info(reader)