"""
imageLSB.py
This module provides functions to hide and extract messages in images using the least significant bit (LSB) method.

Matthew Martin mjm836
CS-465-001 SP 24-25
Assignment 3

"""
class EXIT_CODE:
    SUCCESS = 0
    ERROR = 1
    WARNING = 2
    INFO = 3

import sys
from PIL import Image

def main():
    # declarations
    messageLength = 0
    imageCapacity = 0
    img = None
    width = 0
    height = 0

    
    # input validation
    # length of sys.argv should be 4
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <option> <input_image> <message>")
        return EXIT_CODE.ERROR

    # check if option is valid
    if sys.argv[1].lower() not in ["hide", "retrieve"]:
        print(f"Invalid option: {sys.argv[1]}. Use 'hide' or 'retrieve'.")
        return EXIT_CODE.ERROR

    # check if input_image is a valid image file
    if sys.argv[2].endswith(".png") == False:
        print(f"Invalid image file: {sys.argv[2]}. Use a .png file.")
        return EXIT_CODE.ERROR
    # check if input_image exists and can be read
    try:
        img = Image.open(sys.argv[2])
        # Get image dimensions
        width, height = img.size
        # Calculate image capacity for LSB steganography
        # Each pixel has 3 channels (R,G,B), and it will use 1 bit per channel
        imageCapacity = width * height * 3 // 8  # in bytes
    except FileNotFoundError:
        print(f"File not found: {sys.argv[2]}.")
        return EXIT_CODE.ERROR
    except PermissionError:
        print(f"Permission denied: Cannot read {sys.argv[2]}.")
        return EXIT_CODE.ERROR
    except Exception as e:
        print(f"Error reading image: {e}")
        return EXIT_CODE.ERROR

    # check if message is a valid string
    if sys.argv[3].isempty():
        print("Message cannot be empty.")
        return EXIT_CODE.ERROR
    # check if message is too long
    messageLength = len(sys.argv[3])
    if messageLength > imageCapacity:
        print(f"Message is too long. Maximum length is {imageCapacity} bytes.")
        return EXIT_CODE.ERROR 
    # check if message is a valid string
    if not all(c.isprintable() for c in sys.argv[3]):
        print("Message contains non-printable characters.")
        return EXIT_CODE.ERROR

    return 0

if __name__ == "__main__":
    sys.exit(main())
