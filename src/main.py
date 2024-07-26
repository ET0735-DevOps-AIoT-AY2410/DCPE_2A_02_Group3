import time
import threading as Thread
import queue
import time
import requests
import os
import pandas as pd

from hal import hal_lcd as hal_LCD
from hal import hal_keypad as hal_keypad
from hal import hal_rfid_reader as hal_rfid_reader

import keypad
import lcd
import picam
import RFID

products = {}
bank_database = {}

#Empty list to store sequence of keypad presses
shared_keypad_queue = queue.Queue()


def import_bank_database():
    bank_database = pd.read_csv("bank_database.csv")
    return bank_database


def import_supermarket_database():   
    url = 'https://supermarket-backend-xvd6lpv32a-uc.a.run.app/products'

    try:       
        response = requests.get(url)     
        if response.status_code == 200:
            products = response.json()
            return products
        
        else:
            print('Error:', response.status_code)
            return None
        
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None


def main():

    global products 
    global bank_database

    #initalize
    reader = hal_rfid_reader.init()
    hal_keypad.init(keypad.key_pressed)
    keypad_thread = Thread.Thread(target=hal_keypad.get_key)
    keypad_thread.start()
    print("Keypad initialized.")

    products = import_supermarket_database()
    bank_database = import_bank_database()
    total_price = scan_and_get_total_price()
    print("your total price is: $", total_price)

    print("Please scan your card")
    credit_card_info = RFID.read_rfid_info(reader)
    UID = credit_card_info[0]
    print("UID is:", UID)

    acc_info = interfacing_with_bank(UID)

    balance = acc_info['Balance'].values[0]
    Pin = acc_info['Pin'].values[0]

   # check if amount is sufficent to move on with transaction
    if (balance < total_price):
        print("payment unable to be processed : insufficent bank balance")
        return None
    
    #select payment method
    print("Select payment method")
    print("Paywave: press 1 , Pincode: press 2")
    key_value = keypad.return_key_value()
    if (key_value == 1):
        pay_via_paywave(UID,balance,total_price)

    if (key_value ==2):
        pay_via_pin(UID,balance,Pin,total_price)

    return 


def scan_and_get_total_price():
    
 #   my_picam = picam.initalize_picam()
    total_price = 0

    while (True):
        fn = os.path.basename("barcode.jpg")
      #  picam.capture_image(my_picam)
        barcode_info = picam.decode_barcode(fn)
        print("barcode information:", barcode_info)

        if (barcode_info == "no barcodes detected"):
            continue

        total_price += (products[int(barcode_info)]['price'])
        print("Item Scanned:" , products[int(barcode_info)]['name'],"Price:",products[int(barcode_info)]['price'],"Updated Total:", total_price)

        lcd.display_item_details(products[int(barcode_info)]['name'],products[int(barcode_info)]['price'], total_price)

        print("Press # to stop scanning items")
        # method to exit loop 
        key_value = keypad.return_key_value_no_wait()
        
        if (key_value == "#"):

            break 

    return total_price


def interfacing_with_bank(UID):
    card_info = bank_database.loc[bank_database["UID"] == int(UID)]
    return card_info


def pay_via_paywave(UID,balance,total_price):

    print("Payment via paywave selected") 
    print(interfacing_with_bank(UID))        
    new_balance = balance - total_price
    print("Current balance is:" , balance)

    bank_database.loc[bank_database['UID'] == int(UID),'Balance'] = new_balance
    bank_database.to_csv("bank_database.csv", index=False)

    print("Updated balance:", new_balance)
    print(interfacing_with_bank(UID)) 
    print("Payment_successful")
    print("Thank you, have a nice day!")
    return
    
def pay_via_pin(UID,balance,Pin,total_price):

    print("payment via pincode selected")
    print(interfacing_with_bank(UID)) 
    new_balance = balance - total_price
    keypad.print_keypad_input(Pin)

    bank_database.loc[bank_database['UID'] == int(UID),'Balance'] = new_balance
    bank_database.to_csv("bank_database.csv", index=False)

    print("Updated balance:", new_balance)
    print(interfacing_with_bank(UID)) 
    print("payment successful")
    return

if __name__ == '__main__':
    main()


