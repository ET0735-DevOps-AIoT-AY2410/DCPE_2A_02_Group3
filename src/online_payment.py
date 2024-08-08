import picam
import RFID
import os
from PIL import Image
from pyzbar.pyzbar import decode



def main():
    my_picam = picam.initalize_picam()
    while (True):
        fn = os.path.basename("barcode.jpg")
        picam.capture_image(my_picam)

        qr_code = picam.decode_barcode(fn)

        if (qr_code == "no qr code detected"):
            continue

        image = Image.open(fn)
        decoded_qr_code = decode(image)
        print(decoded_qr_code)

        return decoded_qr_code
    
if __name__ == '__main__': 
    main()
