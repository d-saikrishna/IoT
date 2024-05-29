from gpiozero import LED
import time

led = LED(17) #select the GPIO pin you are using

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

def flash_led(morse_code):
    """Flash LED according to Morse code."""
    for symbol in morse_code:
        if symbol == '.':
            led.on()
            time.sleep(DIT_DURATION)
            led.off()
            time.sleep(DIT_DURATION)
        elif symbol == '-':
            led.on()
            time.sleep(DAH_DURATION)
            led.off()
            time.sleep(DAH_DURATION)
        elif symbol == ' ':
            time.sleep(WORD_SPACE)
        elif symbol == '/':
             time.sleep(LETTER_SPACE)

def main():
    text = input("Enter text to flash in Morse code: ")
    morse_code = text_to_morse(text)
    print(f"Morse Code: {morse_code}")
    flash_led(morse_code)
    
if __name__ == "__main__":
    main()
