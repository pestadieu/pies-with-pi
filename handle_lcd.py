from RPLCD import CharLCD
import time

lcd = CharLCD(cols=16, rows=2, pin_rs=4, pin_e=17, pins_data=[18, 22, 23, 24])

# ~ while True:
    # ~ lcd.write_string("Time: %s" %time.strftime("%H:%M:%S"))
    
def printTime(inputTime):
    print inputTime + "secondes"
    return
