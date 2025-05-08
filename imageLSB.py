"""
imageLSB.py
This module provides functions to hide and extract messages in images using the least significant bit (LSB) method.

Matthew Martin mjm836
CS-465-001 SP 24-25
Assignment 3

Dependencies:
    - Python 3.x
    - Pillow (PIL) library for image processing (This is installed on Drexel's tux)
    - sys module for command line arguments
    - os module for file path manipulation
"""
class EXIT_CODE:
    SUCCESS = 0
    GENERAL_ERROR = 1
    HIDING_ERROR = 2
    RETRIEVING_ERROR = 3

import sys
from PIL import Image
import os

"""
    Hide a message in an image using LSB steganography
    This function takes a PIL Image object and a message string, and hides the message 
    in the image's pixel data in a new image. The message is hidden in the least 
    significant bits of the pixel values.

    Creates a new image with the message hidden in it. The new image is saved with 
    "_new" appended to the filename.
    
    Args:
        image: PIL Image object, already converted to RGB
        message: String to hide in the image
        filepath: String, path to the input image file
        
    Returns:
        EXIT_CODE indicating success or failure
"""
def hide_message(image: Image.Image, message: str, filepath: str) -> EXIT_CODE:
    # declarations
    new_path = ""


    try: 
        print("Hiding message...")
        # get new image name
        new_path = new_image_name(filepath)
        # make copy of image
        # calculate message length
        # add message length to the beginning of the message
        # convert message to binary
        # get image data
        # embed message in image data
        # save new image
    except Exception as e:
        print(f"Error HIDING_ERROR message: {e}")
        return EXIT_CODE.HIDING_ERROR
    return EXIT_CODE.SUCCESS


def retrieve_message(image: Image.Image) -> EXIT_CODE:
    print("Retrieving message...")
    return EXIT_CODE.SUCCESS

"""
    Get a new image name for the output file
    This function takes a file path and returns a new file path with "_new" appended
    to the filename. If the new file path already exists, it prompts the user to
    overwrite the existing file or not.

    Args:
        filepath: String, path to the input image file
    Returns:
        new_path: String, path to the new image file
"""
def new_image_name(filepath: str) -> str:
    # declarations
    new_path = ""
    filename = ""

    filename, _ = os.path.splitext(filepath)
    new_path = f"{filename}_new.png"
    # check if new_path exists already
    if os.path.exists(new_path):
        # Ask user if they want to overwrite the existing file
        response = input(f"File {new_path} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            raise Exception(f"User chose not to overwrite {new_path}")

    return new_path


def main() -> EXIT_CODE:
    # declarations
    messageLength = 0
    imageCapacity = 0
    img = None
    width = 0
    height = 0
    option = ""
    
# input validation
    # length of sys.argv should be 3 or 4
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print(f"Usage: python {sys.argv[0]} <hide/retrieve> <input_image> <message (when HIDING_ERROR)>")
        return EXIT_CODE.GENERAL_ERROR

# check if option is valid
    option = sys.argv[1].lower()
    if option not in ["hide", "retrieve"]:
        print(f"Invalid option: {sys.argv[1]}. Use 'hide' or 'retrieve'.")
        return EXIT_CODE.GENERAL_ERROR
    if option == "hide" and len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} hide <input_image> <message>")
        return EXIT_CODE.GENERAL_ERROR
    if option == "retrieve" and len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} retrieve <input_image>")
        return EXIT_CODE.GENERAL_ERROR

# check if input_image is a valid image file
    if sys.argv[2].endswith(".png") == False:
        print(f"Invalid image file: {sys.argv[2]}. Use a .png file.")
        return EXIT_CODE.GENERAL_ERROR
    # check if input_image exists and can be read
    try:
        img = Image.open(sys.argv[2])
        img = img.convert("RGB")  # Convert to RGB if not already in that mode
        if option == "hide":
            # Get image dimensions
            width, height = img.size
            # Calculate image capacity for LSB steganography
            # Each pixel has 3 channels (R,G,B), and it will use 1 bit per channel
            imageCapacity = width * height * 3 // 8  # in bytes
    except FileNotFoundError:
        print(f"File not found: {sys.argv[2]}.")
        return EXIT_CODE.GENERAL_ERROR
    except PermissionError:
        print(f"Permission denied: Cannot read {sys.argv[2]}.")
        return EXIT_CODE.GENERAL_ERROR
    except Exception as e:
        print(f"Error reading image: {e}")
        return EXIT_CODE.GENERAL_ERROR

# check if message is a valid string
    if option == "hide":
        if not sys.argv[3]:
            print("Message cannot be empty.")
            return EXIT_CODE.GENERAL_ERROR
        # check if message is too long
        messageLength = len(sys.argv[3])
        if messageLength > imageCapacity:
            print(f"Message is too long. Maximum length is {imageCapacity} bytes.")
            return EXIT_CODE.GENERAL_ERROR 
        # check if message is a valid string
        if not all(c.isprintable() for c in sys.argv[3]):
            print("Message contains non-printable characters.")
            return EXIT_CODE.GENERAL_ERROR

    # run the function
    match option:
        case "hide": 
            return hide_message(img, sys.argv[3], sys.argv[2])
        case "retrieve":
            # retrieve the message from the image
            return retrieve_message(img)
        case _:
            print(f"Error in option") # I don't know how it could get here, just covering my bases
            return EXIT_CODE.GENERAL_ERROR

    return EXIT_CODE.SUCCESS

if __name__ == "__main__":
    sys.exit(main())
