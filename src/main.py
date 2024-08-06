import threading as Thread
import queue
import time
import requests
import os
import pandas as pd
from collections import Counter

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
LCD = hal_lcd.lcd()

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

def edit_products(id,amount):
    payload={
            "id":id,
            "Quantity":amount
            }
    requests.put("https://supermarket-backend-xvd6lpv32a-uc.a.run.app/products", params=payload)   
    return

def main():

    global products 

    #initalize
    
    reader = hal_rfid_reader.init()
    hal_keypad.init(keypad.key_pressed)
    keypad_thread = Thread.Thread(target=hal_keypad.get_key)
    keypad_thread.start()
    print("Keypad initialized.")

    # get databases
    products = import_supermarket_database()
    bank_database = import_bank_database()
    
    #scan items and return order request
    order_req = scan_and_get_total_price()
    print("your total price is: $", order_req[0])
    LCD.lcd_clear()
    LCD.lcd_display_string("Total price:" + str(order_req[0]))

    
    # edit database for products purchased
    counts = Counter(order_req[1])  
    combined_list = [f"{num}:{count}" for num, count in counts.items()]
    for item in combined_list:
        id_str, amount_str = item.split(":")
        id = int(id_str)
        amount = int(amount_str)
        inital_quanitity = products[id]['quantity'] - amount
        edit_products(id, inital_quanitity)

    #scan RFID and return UID in order to interface with database
    LCD.lcd_clear()
    LCD.lcd_display_string("Scan your card",1)
    print("Please scan your card")
    credit_card_info = RFID.read_rfid_info(reader)
    UID = credit_card_info[0]
    print("UID is:", UID)
    LCD.lcd_display_string("UID is:" + UID, 1)

    #get balance and Pin number for specfied UID
    acc_info = interfacing_with_bank(bank_database, UID)
    balance = acc_info['Balance'].values[0]
    Pin = acc_info['Pin'].values[0]
    LCD.lcd_display_string("Balance:" + str(balance) ,2)

   # check if amount is sufficent to move on with transaction
    if (balance < order_req[0]):
        print("payment failed: insufficent balance")
        LCD.lcd_display_string("Payment failed:",1)
        LCD.lcd_display_string("Insufficent funds",2)

        return None
    #Keep infomation on LCD for 1s
    time.sleep(1)

    #select payment method and choose accordingly
    print("Select payment method")
    print("Paywave: press 1 , Pincode: press 2")
    LCD.lcd_clear()
    LCD.lcd_display_string("Payment method",1)
    LCD.lcd_display_string("1:Paywave 2:Pin",2)

    #Get input from keypad
    key_value = keypad.return_key_value()
    #paywave case
    if (key_value == 1):
        pay_via_paywave(bank_database,UID,balance,order_req[0])
    #pin case
    if (key_value ==2):
        pay_via_pin(bank_database,UID,balance,Pin,order_req[0])

    return 


def scan_and_get_total_price():
    #initalise picam and vairables
  #  my_picam = picam.initalize_picam()
    total_price = 0
    order = [] 

    while (True):
        LCD.lcd_clear()
        LCD.lcd_display_string("Scan items")
        #set file path and capture image to file path
        fn = os.path.basename("barcode.jpg")
       # picam.capture_image(my_picam)

        #decode barcode and continue loop if no barcodes
        barcode_info = picam.decode_barcode(fn)
        barcode_info = int(barcode_info)
        print("barcode information:", barcode_info)
        if (barcode_info == "no barcodes detected"):
            continue
        
        #print important information related to product
        total_price += (products[barcode_info]['price'])
        print("Item Scanned:" , products[barcode_info]['name'],"Price:",products[barcode_info]['price'],"Updated Total:", total_price)
       
        #add product to "order" to keep track of purchases to later edit database
        order.append(barcode_info) 
        lcd.display_item_details(products[barcode_info]['name'],products[barcode_info]['price'], total_price)

        #Display LCD info for 2s
        time.sleep(2)
        # method to exit loop 
        key_value = keypad.return_key_value_no_wait()
        
        if (key_value == "#"):
            break 

    return total_price,order


def interfacing_with_bank(bank_database, UID):
    card_info = bank_database.loc[bank_database["UID"] == int(UID)]
    return card_info


def pay_via_paywave(bank_database,UID,balance,total_price):

    print("Payment via paywave selected")
    LCD.lcd_clear() 
    LCD.lcd_display_string("Paywave chosen", 1)

    #Calculate new balance
    new_balance = balance - total_price
    print("Current balance is:" , balance)

    #updated bank database with new customer balance
    bank_database.loc[bank_database['UID'] == int(UID),'Balance'] = new_balance
    bank_database.to_csv("bank_database.csv", index=False)

    print("Updated balance:", new_balance)
    LCD.lcd_display_string("New balance" + str(new_balance),2)

    print("Payment successful")
    print("Thank you, have a nice day!")
    #Keep previous message on LCD for 1s
    time.sleep(1)
    LCD.lcd_clear()
    LCD.lcd_display_string("Thank you",1)
    LCD.lcd_display_string("Have a nice day!",2)

    return
    
def pay_via_pin(bank_database,UID,balance,Pin,total_price):

    print("payment via pincode selected")
    LCD.lcd_display_string("Pin chosen", 1)
    LCD.lcd_display_string("Please input your pin" ,2)

    #calculate new balance
    new_balance = balance - total_price
    #Get inputted pin number
    input = keypad.print_keypad_input(Pin)

    #case for correct pin number
    if (input == 1):
        #Update bank database
        bank_database.loc[bank_database['UID'] == int(UID),'Balance'] = new_balance
        bank_database.to_csv("bank_database.csv", index=False)

        print("Updated balance:", new_balance)
        print("Payment successful")
        print("Thank you, have a nice day!")
        LCD.lcd_clear()
        LCD.lcd_display_string("New balance" + str(new_balance),2)

        time.sleep(1)

        LCD.lcd_clear()
        LCD.lcd_display_string("Thank you",1)
        LCD.lcd_display_string("Have a nice day!",2)
        return
    #case for incorrect pin
    if (input== 2):
        return

if __name__ == '__main__':
   main()