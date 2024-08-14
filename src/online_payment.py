import main as my_main
import picam
import RFID
import keypad
import os
import requests 
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

def main():

    reader = hal_rfid_reader.init()
    hal_keypad.init(keypad.key_pressed)
    keypad_thread = Thread.Thread(target=hal_keypad.get_key)
    keypad_thread.start()
    print("Keypad initialized.")

    info = my_main.import_bank_database()
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

    acc_info = my_main.interfacing_with_bank(bank,UID)
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
        my_main.pay_via_paywave(headers,bank,UID,float(balance),total_price)
    #pin case
    if (key_value ==2):
        my_main.pay_via_pin(headers,bank,UID,float(balance),int(Pin),total_price)

    return     
    
def decode_qr_code():
    #my_picam = picam.initalize_picam()

    while (True):
        fn = os.path.basename("qr_code.jpg")
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
             
def paid_order(id):
    try:
        url = 'https://supermarket-backend-xvd6lpv32a-uc.a.run.app/orders/paid/' + str(id)
        print(url)

        response = requests.put(url)
        
        if response.status_code == 200:
            return True
        else:
            raise Exception("Is the backend running?")
    except Exception as e:
        print(f"Error: {e}")
        return False
    
if __name__ == '__main__': 
    paid_order(8)