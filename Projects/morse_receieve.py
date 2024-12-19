from gpiozero import LED
import time
import RPi.GPIO as GPIO

BeepPin = 17

def setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set LedPin's mode to output,
    # and initial level to High(3.3v)
    GPIO.setup(BeepPin, GPIO.OUT, initial=GPIO.HIGH)

# Define the Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-', '!': '-.-.--', '@': '.--.-.',
    ' ': ' '  # Space for separation between words
}

# Define time units
DIT_DURATION = 0.3   # duration of a dit
DAH_DURATION = DIT_DURATION * 3   # duration of a dah
LETTER_SPACE = DIT_DURATION * 3   # space between letters
WORD_SPACE = DIT_DURATION * 7     # space between words

def text_to_morse(text):
    """Convert text to Morse code."""
    morse_code = []
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_code.append(MORSE_CODE_DICT[char])
    return '/'.join(morse_code)

def beep_morse(morse_code):
    """Flash LED according to Morse code."""
    for symbol in morse_code:
        if symbol == '.':
            GPIO.output(BeepPin, GPIO.LOW)
            time.sleep(DIT_DURATION)
            GPIO.output(BeepPin, GPIO.HIGH)
            time.sleep(DIT_DURATION)
        elif symbol == '-':
            GPIO.output(BeepPin, GPIO.LOW)
            time.sleep(DAH_DURATION)
            GPIO.output(BeepPin, GPIO.HIGH)
            time.sleep(DIT_DURATION)
        elif symbol == ' ':
            time.sleep(DIT_DURATION) #Space is sourrounded by 2 / anyway
        elif symbol == '/':
             time.sleep(LETTER_SPACE)

def destroy():
    # Turn off buzzer
    GPIO.output(BeepPin, GPIO.HIGH)
    # Release resource
    GPIO.cleanup()

def main():
    text = input("Enter text to flash in Morse code: ")
    morse_code = text_to_morse(text)
    print(f"Morse Code: {morse_code}")
    beep_morse(morse_code)
    
if __name__ == "__main__":
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the child program
    # destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()
