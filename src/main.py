import threading as Thread
import queue
import time
import requests
import os
import csv
from collections import Counter
from flask import jsonify

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
    database = []
    with open('bank_database.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Read the header row
        for row in csv_reader:
            database.append(dict(zip(headers, row)))
    return database,headers

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
            "id":id+1,
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
    LCD.lcd_display_string("Welcome")
    time.sleep(1)


    # get databases
    products = import_supermarket_database()
    info = import_bank_database()
    bank = info[0]
    headers = info[1]
    
    #scan items and return order request
    order_req = scan_and_get_total_price()
    print("your total price is: $", order_req[0])
    LCD.lcd_clear()
    LCD.lcd_display_string("Total price:" + str(order_req[0]))

    
    # edit supermarket database for products purchased
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
    acc_info = interfacing_with_bank(bank,UID)
    balance = acc_info['Balance']
    Pin = acc_info['Pin']
    LCD.lcd_display_string("Balance:" + str(balance) ,2)

   # check if amount is sufficent to move on with transaction
    if (float(balance) < order_req[0]):
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

    key_value = keypad.return_key_value()

    while key_value != 1 and key_value != 2:
            print("wrong key inputted, try again")
            key_value = keypad.return_key_value()
            print(key_value)
        
    #paywave case
    if (key_value == 1):
        pay_via_paywave(headers,bank,UID,float(balance),order_req[0])
    #pin case
    if (key_value ==2):
        pay_via_pin(headers,bank,UID,float(balance),int(Pin),order_req[0])

    return 

def scan_and_get_total_price():
    #initalise picam and vairables
 #   my_picam = picam.initalize_picam()
    total_price = 0
    order = [] 

    while (True):
        LCD.lcd_clear()
        LCD.lcd_display_string("Scan your items")
        #set file path and capture image to file path
        fn = os.path.basename("barcode.jpg")
    #    picam.capture_image(my_picam)

        #decode barcode and continue loop if no barcodes
        barcode_info = picam.decode_barcode(fn)
        if (barcode_info == "nothing detected"):

            time.sleep(1)
            key_value = keypad.return_key_value_no_wait()

            if (key_value == "#"):
                break 

            continue
        barcode_info = int(barcode_info) -1
        print("barcode information:", barcode_info)       
        
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

def interfacing_with_bank(bank,UID):
    for record in bank:
        if record['UID'] == UID:
            return record
    return "UID not found"

def pay_via_paywave(headers,bank,UID,balance,total_price):

    print("Payment via paywave selected")
    time.sleep(1)
    LCD.lcd_clear() 
    LCD.lcd_display_string("Paywave chosen", 1)

    #Calculate new balance
    new_balance = balance - total_price
    print("Current balance is:" , balance)

    #updated bank database with new customer balance
    update_balance(headers,bank,UID,new_balance)

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
    
def pay_via_pin(headers,bank,UID,balance,Pin,total_price):

    print("payment via pincode selected")
    time.sleep(1)
    LCD.lcd_clear()
    LCD.lcd_display_string("Pin chosen", 1)
    LCD.lcd_display_string("Enter Pin" ,2)

    #calculate new balance
    new_balance = balance - total_price
    #Get inputted pin number
    input = keypad.print_keypad_input(Pin)

    #case for correct pin number
    if (input == 1):
        #Update bank database
        update_balance(headers,bank,UID,new_balance)

        print("Updated balance:", new_balance)
        print("Payment successful")
        print("Thank you, have a nice day!")
        LCD.lcd_clear()
        LCD.lcd_display_string("Balance:" + str(new_balance),1)

        time.sleep(1)

        LCD.lcd_clear()
        LCD.lcd_display_string("Thank you",1)
        LCD.lcd_display_string("Have a nice day!",2)
        return
    #case for incorrect pin
    if (input== 2):
        return

def update_balance(headers,bank,UID,new_balance):
    for record in bank:
        if record['UID'] == UID:
            record['Balance'] = str(new_balance)
            break
    with open('bank_database.csv', mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(headers)  # Write the header row
        for record in bank:
            csv_writer.writerow([record[header] for header in headers])        


if __name__ == '__main__': 
    main()
