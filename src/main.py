import threading as Thread
import queue
import time
import requests
import os
import pandas as pd

from hal import hal_lcd
from hal import hal_keypad as hal_keypad
from hal import hal_rfid_reader as hal_rfid_reader

import keypad
import lcd
import picam
import RFID

products = {}

#Empty list to store sequence of keypad presses
shared_keypad_queue = queue.Queue()


def import_bank_database():
    bank_database = pd.read_csv("bank_database.csv")
    return pd.DataFrame(bank_database)


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

    #initalize
    LCD = hal_lcd.lcd()
    reader = hal_rfid_reader.init()
    hal_keypad.init(keypad.key_pressed)
    keypad_thread = Thread.Thread(target=hal_keypad.get_key)
    keypad_thread.start()
    print("Keypad initialized.")

    # get databases
    products = import_supermarket_database()
    bank_database = import_bank_database()
    
    #scan items and return total price
    total_price = scan_and_get_total_price()
    print("your total price is: $", total_price)

    #scan RFID and return UID in order to interface with database
    LCD.lcd_clear()
    LCD.lcd_display_string("Please scan your card",1)
    print("Please scan your card")
    credit_card_info = RFID.read_rfid_info(reader)
    UID = credit_card_info[0]
    print("UID is:", UID)

    #get balance and Pin number for specfied UID
    acc_info = interfacing_with_bank(bank_database, UID)
    balance = acc_info['Balance'].values[0]
    Pin = acc_info['Pin'].values[0]

   # check if amount is sufficent to move on with transaction
    if (balance < total_price):
        print("payment unable to be processed : insufficent bank balance")
        return None
    
    #select payment method and choose accordingly
    print("Select payment method")
    print("Paywave: press 1 , Pincode: press 2")
    
    LCD.lcd_clear()
    LCD.lcd_display_string("Select Payment method",1)
    LCD.lcd_display_string("1: paywave 2: Pin",2)

    key_value = keypad.return_key_value()
    if (key_value == 1):
        pay_via_paywave(bank_database,UID,balance,total_price)

    if (key_value ==2):
        pay_via_pin(bank_database,UID,balance,Pin,total_price)

    return 


def scan_and_get_total_price():
    
  #  my_picam = picam.initalize_picam()
    total_price = 0

    while (True):

        fn = os.path.basename("barcode.jpg")
       # picam.capture_image(my_picam)
        barcode_info = picam.decode_barcode(fn)
        print("barcode information:", barcode_info)

        if (barcode_info == "no barcodes detected"):
            continue
        
        total_price += (products[int(barcode_info)]['price'])
        print("Item Scanned:" , products[int(barcode_info)]['name'],"Price:",products[int(barcode_info)]['price'],"Updated Total:", total_price)

        lcd.display_item_details(products[int(barcode_info)]['name'],products[int(barcode_info)]['price'], total_price)

        time.sleep(2)
        # method to exit loop 
        key_value = keypad.return_key_value_no_wait()
        
        if (key_value == "#"):
            break 

    return total_price


def interfacing_with_bank(bank_database, UID):
    card_info = bank_database.loc[bank_database["UID"] == int(UID)]
    return card_info


def pay_via_paywave(bank_database,UID,balance,total_price):

    print("Payment via paywave selected") 
    #print intial values (for personal reference)
    new_balance = balance - total_price
    print("Current balance is:" , balance)

    bank_database.loc[bank_database['UID'] == int(UID),'Balance'] = new_balance
    bank_database.to_csv("bank_database.csv", index=False)

    print("Updated balance:", new_balance)
    print("Payment_successful")
    print("Thank you, have a nice day!")
    return
    
def pay_via_pin(bank_database,UID,balance,Pin,total_price):

    print("payment via pincode selected")
    #print intial values (for personal reference)
    new_balance = balance - total_price
    input = keypad.print_keypad_input(Pin)

    if (input == 1):
        bank_database.loc[bank_database['UID'] == int(UID),'Balance'] = new_balance
        bank_database.to_csv("bank_database.csv", index=False)

        print("Updated balance:", new_balance)
        print("payment successful")
        return
    if (input== 2):
        return

if __name__ == '__main__':
    main()


