from gpiozero import Button, LED
import RPi.GPIO as GPIO
from signal import pause
from time import sleep
led = LED(17)
button = Button(21, bounce_time = 0.1) # Debounce buttons

def toggle_led():
    led.toggle()
    print('Button pressed!')
    while button.is_pressed == True:
        pass

button.when_pressed = toggle_led

pause()
