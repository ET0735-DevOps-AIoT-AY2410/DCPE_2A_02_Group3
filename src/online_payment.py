import main as my_main
import picam
import RFID
import keypad
import os
import csv
import queue
import threading as Thread
from PIL import Image
from pyzbar.pyzbar import decode
import time

from hal import hal_lcd
import hal.hal_rfid_reader as hal_rfid_reader
from hal import hal_keypad as hal_keypad


LCD = hal_lcd.lcd()
shared_keypad_queue = queue.Queue()

bank = {}
headers = {}


def main():
    global bank 
    global headers


    reader = hal_rfid_reader.init()
    hal_keypad.init(keypad.key_pressed)
    keypad_thread = Thread.Thread(target=hal_keypad.get_key)
    keypad_thread.start()
    print("Keypad initialized.")

    info = import_bank_database()
    bank = info[0]
    headers = info[1]

    qr_code_data = decode_qr_code()
    qr_code_data =  [int(x) for x in qr_code_data.split(',')]
    print(qr_code_data[1])
    total_price = float(qr_code_data[1])
    print(total_price)

    LCD.lcd_clear()
    LCD.lcd_display_string("Scan your card",1)
    print("Please scan your card")

    credit_card_info = RFID.read_rfid_info(reader)
    UID = credit_card_info[0]

    print("UID is:", UID)
    LCD.lcd_display_string("UID is:" + UID, 1)
    #get balance and Pin number for specfied UID

    acc_info = interfacing_with_bank(UID)
    print(acc_info)
    balance = acc_info['Balance']
    Pin = acc_info['Pin']
    LCD.lcd_display_string("Balance:" + str(balance) ,2)

       # check if amount is sufficent to move on with transaction
    if (float(balance) < total_price):
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

    if (key_value == 1):
        pay_via_paywave(UID,float(balance),total_price)
    #pin case
    if (key_value ==2):
        pay_via_pin(UID,float(balance),int(Pin),total_price)

    return     
    
def decode_qr_code():
    #my_picam = picam.initalize_picam()

    while (True):
        fn = os.path.basename("barcode.jpg")
   #     picam.capture_image(my_picam)

        qr_code = picam.decode_barcode(fn)
        
        if (qr_code == "nothing detected"):
            print("no qr detected")
            continue

        image = Image.open(fn)
        decoded_qr_code = decode(image)
        qr_code_data = decoded_qr_code[0].data.decode('utf-8')

        if decoded_qr_code:
            print("qr code data:" , qr_code_data)
            return qr_code_data
        
def interfacing_with_bank(UID):
    for record in bank:
        if record['UID'] == UID:
            return record
    return "UID not found"        

def import_bank_database():
    database = []
    with open('bank_database.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Read the header row
        for row in csv_reader:
            database.append(dict(zip(headers, row)))
    return database,headers

def update_balance(UID,new_balance):
    for record in bank:
        if record['UID'] == UID:
            record['Balance'] = str(new_balance)
            break
    with open('bank_database.csv', mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(headers)  # Write the header row
        for record in bank:
            csv_writer.writerow([record[header] for header in headers])       

def pay_via_paywave(UID,balance,total_price):

    print("Payment via paywave selected")
    time.sleep(1)
    LCD.lcd_clear() 
    LCD.lcd_display_string("Paywave chosen", 1)

    #Calculate new balance
    new_balance = balance - total_price
    print("Current balance is:" , balance)

    #updated bank database with new customer balance
    update_balance(UID,new_balance)

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

def pay_via_pin(UID,balance,Pin,total_price):

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
        update_balance(UID,new_balance)

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

if __name__ == '__main__': 
    main()