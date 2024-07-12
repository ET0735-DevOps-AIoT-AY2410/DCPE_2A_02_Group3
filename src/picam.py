from picamera2.encoders import H264Encoder
from picamera2 import Picamera2, Preview
import time
from PIL import Image
from pyzbar.pyzbar import decode
import os

def capture_image():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)},
    lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    picam2.capture_file("barcode.jpg")

def decode_barcode(file):
    image = Image.open(file)
    scanned_barcode = decode(image)
    
    for barcode in scanned_barcode:
        barcode_data = barcode.data.decode()
        print("barcode:", barcode_data)
    return barcode_data


if __name__ == "__main__":
    fn = os.path.basename("barcode.jpg")
    capture_image()
    decode_barcode(fn)