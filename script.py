import time
import handle_lcd as hl

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
    return 3

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
