from PIL import Image
from pyzbar.pyzbar import decode
import os


    #decode barcode from picture
def decode_barcode(file):
    image = Image.open(file)
    scanned_barcode = decode(image)
    barcode_data = 0 
    
    if (len(scanned_barcode) == 0):
        print ("nothing detected")
        return "nothing detected"

    for barcode in scanned_barcode:
        barcode_data = barcode.data.decode()

    return barcode_data


if __name__ == "__main__":
    fn = os.path.basename("barcode.jpg")

    decode_barcode(fn)