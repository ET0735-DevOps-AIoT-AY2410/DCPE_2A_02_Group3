This is Pavens Branch

HARDWARE REQUIRMENTS

RPI 4 
1. Picam -> used for deocding barcode and qr code
2. RFID -> used for payment functionality by interfacing with csv database
3. Keypad -> Used for payment in pin requriment by inputting pin number
4. LCD -> General use in displaying instructions for user to interact

Explanation of code:
Initalise some Modules
Import supermarket database using API and import CSV
Scan items using barcode and get scanned item information from database
Edit scanned products in database
Scan RFID card and get UID from bank
Check wether balance is sufficent to move forward
Pay with either pin or paywave
If using pin enter pin and pay


