import queue
import threading as Thread
from hal import hal_keypad as keypad
import time


shared_keypad_queue = queue.Queue()

def dummy_info():
    A = int(1234)
    return A

def key_pressed(key):
    shared_keypad_queue.put(key)

def read_keypad():
    print("Initializing keypad...")
    keypad.init(key_pressed)
    print("Keypad initialized.")

    keypad_thread = Thread.Thread(target=keypad.get_key)
    keypad_thread.start()
    

def print_keypad_input(card_pin):
    input_pin = []
    print("Waiting for key press...")

    #change card_pin into list so len function can be used
    while (len(input_pin) < len([int(i) for i in str(card_pin)])):
        key_value = shared_keypad_queue.get()
        input_pin.append(key_value)
        print("Next input")
    
    print("pin inputted:" , input_pin)
    #change input_pin from type list to int
    converted_input_pin = int(''.join(map (str,input_pin)))

    #different cases based on possible outcomes
    print(converted_input_pin)
    if (card_pin == converted_input_pin):
        print("successful: correct pin inputted")
        return 1

    elif (card_pin != converted_input_pin):
        print("Unsuccesful: wrong pin inputted")
        return 2

    else: 
        print("error")

#function used in order to get key_value
def return_key_value():
   
    key_value = shared_keypad_queue.get()
    print(key_value)
    return key_value

#function used in order to get key_value without stopping code from progressing
def return_key_value_no_wait():
    try:
        time.sleep(1)
        key_value = shared_keypad_queue.get_nowait()
        
    except queue.Empty:
        print("continuing loop")
        return
    print(key_value)
    return key_value

if __name__ == '__main__': 
    print("Initializing keypad...")
    keypad.init(key_pressed)
    print("Keypad initialized.")

    keypad_thread = Thread.Thread(target=keypad.get_key)
    keypad_thread.start()

    card_pin = 1234
    print_keypad_input(card_pin)