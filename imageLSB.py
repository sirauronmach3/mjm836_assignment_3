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

def main():
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
    # not sure how to check if a file is an image

    # check if message is a valid string
    if sys.argv[3].isempty():
        print("Message cannot be empty.")
        return EXIT_CODE.ERROR

    return 0

if __name__ == "__main__":
    sys.exit(main())
