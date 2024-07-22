import time
import threading as Thread
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

fruits = {
    1: {"name": "apple", "price": 1.20},
    2: {"name": "orange", "price": 0.80},
    3: {"name": "watermelon", "price": 4.00},
    4: {"name": "pineapple", "price": 3.50},
    5: {"name": "pear", "price": 1.50},
    6: {"name": "papaya", "price": 2.75},
    7: {"name": "pomegranate", "price": 3.00}
}


#Empty list to store sequence of keypad presses
shared_keypad_queue = queue.Queue()


def import_database():

     # Define the API endpoint URL
    url = 'https://supermarket-backend-xvd6lpv32a-uc.a.run.app/products'

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
        
    except requests.exceptions.RequestException as e:
  
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return None



def main():

    reader = hal_rfid_reader.init()
    hal_keypad.init(keypad.key_pressed)


    keypad_thread = Thread.Thread(target=hal_keypad.get_key)
    keypad_thread.start()
    print("Keypad initialized.")

    total_price = scan_and_get_total_price()

    print("please scan your card")
    credit_card_info = RFID.read_rfid_info(reader)
    
   # check if amount is sufficent to move on with transaction
    if (credit_card_info[1][0] < total_price):
        print("payment unable to be processed : insufficent bank balance")
    
    print("Select payment method")
    print("Paywave: press 1 , Pincode: press 2")
    key_value = keypad.return_key_value()

    #select payment method
    print("Select payment method")
    print("Paywave: press 1 , Pincode: press 2")
    key_value = keypad.return_key_value()
    if (key_value == 1):
        pay_via_paywave()

    if (key_value ==2):
        pay_via_pin()

    return


def scan_and_get_total_price():
    while (True):
        fn = os.path.basename("barcode.jpg")
        # picam.capture_image
        barcode_info = picam.decode_barcode(fn)
        #insert code to interface thru database and find product with name and cost print lcd name and cost and add price to total price
        total_price = 5
        print("do you want to exit loop?")
        # method to exit loop 
        key_value = keypad.return_key_value()
        
        if (key_value == "#"):
            break 
    return total_price

def pay_via_paywave(credit_card_info,total_price,reader):

    print(" payment via paywave selected")         
    new_credit_card_balance = credit_card_info[1][0] - total_price
    print("Updated balance:", new_credit_card_balance)
    RFID.Write_data_to_rfid(reader,new_credit_card_balance)
    print("payment_successful")
    return
    
def pay_via_pin(credit_card_info,total_price,reader):

    print("payment via pincode selected")
    new_credit_card_balance = credit_card_info[1][0] - total_price
    print("Updated balance:", new_credit_card_balance)
    keypad.print_keypad_input(1234)
    RFID.Write_data_to_rfid(reader,new_credit_card_balance)
    print("payment successful")
    return


if __name__ == '__main__':
    products = import_database()

    if products:
        print(products)
    
    else: 
        print("failed to fetch db")