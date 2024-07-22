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
      B = cleaned_A[1]
      split_B = B.split(',')

      #assign variables
      uid = cleaned_A[0]
      card_data = [int(item) for item in split_B[:-1]]
      pin = split_B[-1]

      #print data
      print("uid of card:",uid)
      print("data stored on card:", card_data) 
      print("pin of this card:", pin)

      return uid,card_data,pin


def Write_data_to_rfid(reader,new_balance):
      ignore_stdout = sys.stdout
      sys.stdout = open('trash' , 'w')
      reader.write(str(new_balance) + ',4465594948671029' + '1234 ')
      sys.stdout.close()
      sys.stdout = ignore_stdout


if __name__ == "__main__":
      reader = rfid_reader.init()
      read_rfid_info(reader)