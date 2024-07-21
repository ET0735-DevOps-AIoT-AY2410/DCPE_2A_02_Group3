import queue
from hal import hal_keypad as keypad
import threading as Thread

shared_keypad_queue = queue.Queue()

def dummy_info():
    A = int(1234)
    return A

def key_pressed(key):
    shared_keypad_queue.put(key)

def print_keypad_input(card_pin):
    print("Initializing keypad...")
    keypad.init(key_pressed)
    print("Keypad initialized.")
    
    keypad_thread = Thread.Thread(target=keypad.get_key)
    keypad_thread.start()

    #store pin as list and append list and inputs are pressed
    input_pin = []
    while (len(input_pin)<4):
        print("Waiting for key press...")

        key_value = shared_keypad_queue.get()
        input_pin.append(key_value)
    
    print("pin inputted:" , input_pin)
    #convert list to int
    converted_input_pin = int(''.join(map (str,input_pin)))

    print(converted_input_pin)
    
    if (card_pin == converted_input_pin):
        print("successful")

    elif (card_pin != converted_input_pin):
        print("Unsuccesful: wrong pin inputted")

    else: 
        print("error")

if __name__ == '__main__':

    card_pin = dummy_info()
    print_keypad_input(card_pin)