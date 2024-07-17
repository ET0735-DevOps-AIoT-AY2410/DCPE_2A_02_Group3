import time
from threading import Thread
import queue
import time
import requests
import os

from hal import hal_lcd as hal_LCD
from hal import hal_keypad as hal_keypad
from hal import hal_rfid_reader as hal_rfid_reader

import keypad
import lcd
import picam
import RFID



#Empty list to store sequence of keypad presses
shared_keypad_queue = queue.Queue()


def import_database():
    response = requests.get("https://localhost:5000/produdcts")
    return response.json() 


#Call back function invoked when any key on keypad is pressed
def key_pressed(key):
    shared_keypad_queue.put(key)


def main():

    reader = hal_rfid_reader.init()
    keypad.read_keypad()


    while (True):
        fn = os.path.basename("barcode.jpg")
        # picam.capture_image
        barcode_info = picam.decode_barcode(fn)

        total_price = 0
        #insert code to interface thru database and find product with name and cost print lcd name and cost and add price to total price
        print("do you want to exit loop?")
        
        # method to exit loop 
        key_value = keypad.return_key_value()
        print(key_value)
        if (key_value == "#"):
            break   
    
    # check if amount is sufficent to move on with transaction
    credit_card_info = RFID.read_rfid_info(reader)
    print("im here")
    if (credit_card_info[1] <= total_price):
        print("payment unable to be processed : insufficent bank balance")

    #select payment method
    if (key_value == "1"):
        print(" payment via pin code selected")

        if (credit_card_info[1] >= total_price):
            print("payment_successful")

            new_credit_card_balance = credit_card_info[1] - total_price
            RFID.Write_data_to_rfid(new_credit_card_balance)

    if (key_value == "2"):
        print("payment via paywave selected")
        
        if (credit_card_info[1] >= total_price):
            keypad.print_keypad_input()
            print("payment successful")

  

if __name__ == '__main__':
    main()