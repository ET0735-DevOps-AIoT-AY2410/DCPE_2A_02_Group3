from picamera2 import Picamera2, Preview
import time
from PIL import Image
from pyzbar.pyzbar import decode
import os
import sys


def initalize_picam():
    time.sleep(5)
    ignore_stdout = sys.stdout
    sys.stdout = open('trash', 'w')
    picam2 = Picamera2()
    picam2.resolution = (1440, 1080)
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)},
    lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    sys.stdout.close()
    sys.stdout = ignore_stdout
    return picam2


def capture_image(picam2):
    time.sleep(3)
    picam2.capture_file("barcode.jpg")


def decode_barcode(file):
    image = Image.open(file)
    scanned_barcode = decode(image)
    barcode_data = 0 
    
    if (len(scanned_barcode) == 0):
        print ("no barcodes detected")
        return "no barcodes detected"

    for barcode in scanned_barcode:
        barcode_data = barcode.data.decode()
        print("barcode information:", barcode_data)
    
    return barcode_data


if __name__ == "__main__":
    fn = os.path.basename("barcode.jpg")
    picam2 = initalize_picam()
    capture_image(picam2)
    decode_barcode(fn)