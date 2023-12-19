import pywhatkit as py
import keyboard
import time
from datetime import datetime


def sendMessage(numbers, message, price):
    for number in numbers:
        py.sendwhatmsg(number, "{}: {:.10f}".format(message, price), datetime.now().hour,
                       datetime.now().minute + 2)
        keyboard.press_and_release('ctrl+w')
        time.sleep(1)
        keyboard.press_and_release('enter')
        time.sleep(1)
