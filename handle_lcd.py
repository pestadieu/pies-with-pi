from RPLCD import CharLCD
import time
import RPi.GPIO as GPIO

lcd = CharLCD(cols=16, rows=2, pin_rs=4, pin_e=17, pins_data=[18, 22, 23, 24], numbering_mode=GPIO.BCM)

# ~ while True:
    # ~ lcd.write_string("Time: %s" %time.strftime("%H:%M:%S"))

def printTime(inputTime):
    clear()
    lcd.write_string(str(inputTime) + " seconds")
    return

def clear():
    lcd.cursor_pos = (0,0)
    lcd.write_string(" " * 16)
    lcd.cursor_pos = (1, 0)
    lcd.write_string(" " * 16)
    lcd.cursor_pos = (0, 0)
    return

def short_clear()
    lcd.cursor_pos = (0,0)
    lcd.write_string(" " * 16)
    lcd.cursor_pos = (0, 0)
    return

if __name__ == "__main__":
    clear()
    printTime(5)
    time.sleep(3)
    clear()
    printTime(45)
    time.sleep(2)
    clear()
