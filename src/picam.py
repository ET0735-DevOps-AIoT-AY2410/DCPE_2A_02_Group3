from picamera2 import Picamera2, Preview
import time
from PIL import Image
from pyzbar.pyzbar import decode
import os


def initalize_picam():
    picam2 = Picamera2()

    #configure settings for resolutions and display of picam and display
    picam2.resolution = (1440, 1080)
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)},
    lores={"size": (640, 480)}, display="lores")

    #turn on camera
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    return picam2

    #take picture after waiting for 3s (giving the user time to set up barcode)
def capture_image(picam2):
    time.sleep(3)
    picam2.capture_file("barcode.jpg")

    #decode barcode from picture
def decode_barcode(file):
    image = Image.open(file)
    scanned_barcode = decode(image)
    barcode_data = 0 
    
    if (len(scanned_barcode) == 0):
        print ("no barcodes detected")
        return "no barcodes detected"

    for barcode in scanned_barcode:
        barcode_data = barcode.data.decode()

    return barcode_data


if __name__ == "__main__":
    fn = os.path.basename("barcode.jpg")
    #picam2 = initalize_picam()
    #capture_image(picam2)
    decode_barcode(fn)