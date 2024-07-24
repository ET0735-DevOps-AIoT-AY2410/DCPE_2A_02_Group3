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

#Empty list to store sequence of keypad presses
shared_keypad_queue = queue.Queue()


def import_bank_database():
    bank_database = pd.read_csv("Bank_database.csv")
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

    #initalize
    reader = hal_rfid_reader.init()
    hal_keypad.init(keypad.key_pressed)
    keypad_thread = Thread.Thread(target=hal_keypad.get_key)
    keypad_thread.start()
    print("Keypad initialized.")

    products = import_supermarket_database()
    total_price = scan_and_get_total_price()
    print("your total price is:", total_price)

    print("please scan your card")
    credit_card_info = RFID.read_rfid_info(reader)
    
   # check if amount is sufficent to move on with transaction
    if (credit_card_info[1][0] < total_price):
        print("payment unable to be processed : insufficent bank balance")
        return None
    
    #select payment method
    print("Select payment method")
    print("Paywave: press 1 , Pincode: press 2")
    key_value = keypad.return_key_value()
    if (key_value == 1):
        pay_via_paywave(credit_card_info,total_price,reader)

    if (key_value ==2):
        pay_via_pin(credit_card_info,total_price,reader)

    return 


def scan_and_get_total_price():
    
    my_picam = picam.initalize_picam()
    total_price = 0

    while (True):
        fn = os.path.basename("barcode.jpg")
        picam.capture_image(my_picam)
        barcode_info = picam.decode_barcode(fn)
        print("barcode info:", barcode_info)

        if (barcode_info == "no barcodes detected"):
            continue

        total_price += (products[int(barcode_info)]['price'])
        print("item data" , products[int(barcode_info)]['name'],products[int(barcode_info)]['price'], total_price)

        lcd.display_item_details(products[int(barcode_info)]['name'],products[int(barcode_info)]['price'], total_price)

        print("do you want to exit loop?")
        # method to exit loop 
        key_value = keypad.return_key_value_no_wait()
        
        if (key_value == "#"):

            break 

    return total_price

def interfacing_with_bank(bank_database , card_num):
    card_info = bank_database[bank_database["Card Num"] == card_num]
    return card_info


def pay_via_paywave(credit_card_info,total_price,reader):

    print(" payment via paywave selected")         
    new_credit_card_balance = credit_card_info[1][0] - total_price
    
    RFID.Write_data_to_rfid(reader,new_credit_card_balance)
    print("Updated balance:", new_credit_card_balance)
    print("payment_successful")
    return
    
def pay_via_pin(credit_card_info,total_price,reader):

    print("payment via pincode selected")
    new_credit_card_balance = credit_card_info[1][0] - total_price
    
    keypad.print_keypad_input(1234)
    RFID.Write_data_to_rfid(reader,new_credit_card_balance)
    print("Updated balance:", new_credit_card_balance)
    print("payment successful")
    return


if __name__ == '__main__':
    bank_database = import_bank_database()
    print(bank_database)
    card_info = interfacing_with_bank(bank_database , 1234567890123456)
    print (card_info)
    print(type(card_info))
    print(card_info[3])
    bank_database.loc[bank_database["Card Num"] == 1234567890123456,'balance'] == 5000

    
    
