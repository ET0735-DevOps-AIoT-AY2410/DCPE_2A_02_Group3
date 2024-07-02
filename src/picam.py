from picamera2.encoders import H264Encoder
from picamera2 import Picamera2, Preview
import time
import cv2 
from pyzbar.pyzbar import decode


def barcode_scanner ():
    
    # initialise PiCam
    picam2 = Picamera2()

    # initialise video config with 1080p and preview with 480p (preview is live monitor display of picam)
    video_config = picam2.create_video_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(video_config)

    # setup encoder to allow for video to be encoded
    encoder = H264Encoder(bitrate=10000000)
    output = "test.h264"

    # start preview and recording
    picam2.start_preview(Preview.QTGL)
    picam2.start_recording(encoder, output)

    # use while loop to continously record
    while True:
        #capture frame
        frame = picam2.capture
        #convert frame to grayscale
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        #decode information of extracted barcodes
        detected_barcodes = decode(gray)

        #loop through detected barcodes
        for barcode in detected_barcodes: 

            #locate barcode in image
            (x,y,w,h) = barcode.rect

            #put rectangle surrounding barcode 
            cv2.rectangle(frame, ( x + w, y + h), (0, 255, 0), 2)
                          
            #print data and type of scanned barcode
            print("barcode type", barcode.type)
            print(" barcode data", barcode.data)

            #display image of barcode
            cv2.imshow("Barcode", frame)

        # Exit loop if key is pressed
        key_pressed = cv2.waitKey(1) 
        if key_pressed == ord("q"): 
            break
             
    #stop recording and preview
    picam2.stop_recording()
    picam2.stop_preview()