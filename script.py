import time
import os
import handle_lcd as hl
from camera import *
from keras.models import load_model, Sequential
from PIL import Image
import numpy as np

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_NBR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    PIN_NBR = 25
    hl.clear()

def wait_button_pushed():
    while True:
        input_state = GPIO.input(PIN_NBR)
        if input_state == False:
            return
        time.sleep(0.2)

def timer(timeout):
    timelist = range(0, timeout)
    for k in range timeout:
        printTime(timelist[-k])
    return

def camera_read():
    camera.capture("pic.jpg")
    os.system("zbarimg " + "pic.jpg > code.txt")

    with open('code.txt', "r") as text_file:
        data = text_file.readline()

    if not data:
        print("No QR code: Computer vision")
        print("The object is")
        img = Image.open()
        img.resize((100, 100), Image.ANTIALIAS)
        img = np.array(img).astype(np.uint8)
        img = np.expand_dims(img, axis=0)
        model = load_model("fruit_model.h5")
        print(model.predict_classes(img))
        cooking_time = 0
    else:
        data = data.split(":")
        cooking_time = int(data[1])
        print(cooking_time)

    if cooking_time == 0:
        return model.predict_classes(img)
    else:
        return cooking_time

if __name__ == "__main__":
    thread_chat = Chatbot()  # Chatbot thread
    thread_chat.start()
    init()

    t = camera_read()
    wait_button_pushed()
    timer()

    t = camera_read()
    wait_button_pushed()
    timer()

    t = camera_read()
    wait_button_pushed()
    timer()
