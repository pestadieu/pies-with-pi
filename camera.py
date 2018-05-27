import os
import time
from threading import Thread
from queue import Queue
from picamera import PiCamera
from keras.models import load_model, Sequential
import numpy as np
from PIL import Image

camera = PiCamera()

class Camera(Thread):

    def __init__(self, q_write):
        Thread.__init__(self)
        self.name = "camera_thread"
        self.q_write = q_write

    def run(self):
        while True:
            time.sleep(1)
            self.take_photo()
            # Process your photo, do everything you want here
            os.system("zbarimg " + "pic.jpg > code.txt")
            with open('code.txt', "r") as text_file:
                data = text_file.readline()

                if not data:
                    print("no QR code...")
                    print("the fruit is...")
                    img = Image.open("pic.jpg")
                    img = img.resize((100,100), Image.ANTIALIAS)
                    img = np.array(img).astype(np.uint8)
                    img = np.expand_dims(img, axis=0)

                    model = load_model("fruit_model.h5")
                    print(list(model.predict(img)[0]).index(max(model.predict(img)[0])))
                    cooking_time = 0
                else:
                    data = data.split(':')
                    cooking_time = int(data[1])
                    print(cooking_time)

                    #According to the image, put the required cooking time here. If no cooking is required, put 0
                if cooking_time != 0:
                    self.q_write.put(str(cooking_time))

    def take_photo(self):
        camera.capture('pic.jpg')

if __name__ == "__main__":
    camera.capture('pic.jpg')
    os.system("zbarimg " + "pic.jpg > code.txt")

    with open('code.txt', "r") as text_file:
        data = text_file.readline()

    if not data:
        print("not QR code")
    else:
        data = data.split(':')
        print(int(data[1]))
