import RPi.GPIO as GPIO
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
      try:
            # Convert to int; if unable, convert to float
            card_data = [int(item) for item in split_B[:-1]]
      except ValueError:
            card_data = [float(item) for item in split_B[:-1]]      
      
      pin = split_B[-1]

      return uid,card_data,pin


def Write_data_to_rfid(reader):
      ignore_stdout = sys.stdout
      sys.stdout = open('trash' , 'w')
      reader.write("")
      sys.stdout.close()
      sys.stdout = ignore_stdout
      return


if __name__ == "__main__":
      reader = rfid_reader.init()
      Write_data_to_rfid(reader,new_balance=500.0)
      read_rfid_info(reader)

