from gpiozero import Button, LED
import RPi.GPIO as GPIO
from signal import pause
button = Button(21, bounce_time = 0.1) # Debounce buttons

import time
from sys import version_info

if version_info.major == 3:
    raw_input = input


# Set #17 as buzzer pin
BeepPin = 17

def say_hello():
    print('Button pressed!')
    GPIO.output(BeepPin, GPIO.LOW)

def say_goodbye():
    print('Button pressed!')
    GPIO.output(BeepPin, GPIO.HIGH)


def print_message():
    print ("========================================")
    print ("|                 Beep                 |")
    print ("|    ------------------------------    |")
    print ("|        Buzzer connect to GPIO17      |")
    print ("|                                      |")
    print ("|            Make Buzzer beep          |")
    print ("|                                      |")
    print ("|                            SunFounder|")
    print ("======================================\n")
    print ("Program is running...")
    print ("Please press Ctrl+C to end the program...")
    #raw_input ("Press Enter to begin\n")

def setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set LedPin's mode to output,
    # and initial level to High(3.3v)
    GPIO.setup(BeepPin, GPIO.OUT, initial=GPIO.HIGH)

def main():
    print_message()
    button.when_pressed = say_hello
    button.when_released = say_goodbye


    pause()

def destroy():
    # Turn off buzzer
    GPIO.output(BeepPin, GPIO.HIGH)
    # Release resource
    GPIO.cleanup()

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the child program
    # destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()
