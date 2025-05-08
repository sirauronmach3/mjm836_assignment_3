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


import sys
from PIL import Image
import os


class EXIT_CODE:
    SUCCESS = 0
    GENERAL_ERROR = 1
    HIDING_ERROR = 2
    RETRIEVING_ERROR = 3


HEADER_SIZE_BITS = 32
CHAR_SIZE_BITS = 8


"""
    Hide a message in an image using LSB steganography
    This function takes a PIL Image object and a message string, and hides the message 
    in the image's pixel data in a new image. The message is hidden in the least 
    significant bits of the pixel values.

    There is header information, containing message length, that take up the first 32 bits
    of the image. The characters of the message are stored as 8 bit representations of their
    ASCII values.

    Creates a new image with the message hidden in it. The new image is saved with 
    "_new" appended to the filename.
    
    Args:
        image: PIL Image object, already converted to RGB and checked to ensure large enough for message
        message: String to hide in the image
        filepath: String, path to the input image file
        
    Returns:
        EXIT_CODE indicating success or failure
"""
def hide_message(image: Image.Image, message: str, filepath: str) -> EXIT_CODE:
    # declarations
    new_path = ""
    new_image = None
    messageLength = 0
    binaryMessageLength = ""
    binaryMessage = ""
    width = 0
    height = 0
    imageData = None


    try: 
        print("Hiding message...") # TODO: Testing statement, remove this when done
        # get new image name
        new_path = new_image_name(filepath)
        # make copy of image
        new_image = image.copy()
        # calculate message length
        messageLength = len(message)
        binaryLength = format(messageLength, f'0{HEADER_SIZE_BITS}b') # converts message length to a 32 bit binary string
        # convert message to binary
        binaryMessage = get_binary_string(message)
        # append binary length to binary message
        binaryMessage = binaryLength + binaryMessage
        # get image data
        width, height = new_image.size
        imageData = new_image.load()
        # embed message in image data
        if (embed_message(imageData, binaryMessage, width, height) != EXIT_CODE.SUCCESS):
            raise Exception("Error embedding message in image data")
        # save new image
        new_image.save(new_path)
        print(f"Message hidden in {new_path}")
    except Exception as e:
        print(f"Error HIDING_ERROR message: {e}")
        return EXIT_CODE.HIDING_ERROR
    return EXIT_CODE.SUCCESS


def retrieve_message(image: Image.Image) -> EXIT_CODE:
    # declarations
    binaryMessage = ""

    try:
        print("Retrieving message...")
    except Exception as e:
        print(f"Error RETRIEVING_ERROR message: {e}")
        return EXIT_CODE.RETRIEVING_ERROR
    return EXIT_CODE.SUCCESS


"""
    embed_message
    This function takes the image data, a binary message string, and the width and height
    of the image, and embeds the message in the image data. The message is embedded in
    the least significant bits of the pixel values. The function modifies the image data
    in place.


    Modified:
        The image data is modified in place.
    Args:
        imageData: Image data object, a 2D array of pixel values
        binaryMessage: String, binary representation of the message to hide
        width: Integer, width of the image
        height: Integer, height of the image
    Returns:
        EXIT_CODE indicating success or failure
"""
def embed_message(imageData, binaryMessage: str, width: int, height: int) -> EXIT_CODE:
    # declarations
    ordinal = 0
    binaryLength = 0
    i = 0
    j = 0
    r = 0
    g = 0
    b = 0

    binaryLength = len(binaryMessage)
    # loop through pixels in the image
    for i in range(height):
        for j in range(width):
            # get rgb values of pixel
            r, g, b = imageData[j, i]

            # modify each color channel
            # r
            if ordinal < binaryLength:
                # clear the LSB
                r = r & ~1  # bitwise AND with not 1, which clears the LSB
                # set the LSB to the next bit of the message
                r = r | int(binaryMessage[ordinal]) # bitwise OR with the next bit of the message
                # increment ordinal
                ordinal += 1
            # g
            if ordinal < binaryLength:
                g = g & ~1
                g = g | int(binaryMessage[ordinal])
                ordinal += 1
            # b
            if ordinal < binaryLength:
                b = b & ~1
                b = b | int(binaryMessage[ordinal])
                ordinal += 1

            # set the new pixel value
            imageData[j, i] = (r, g, b)
            # check if we have reached the end of the message break inner loop
            if ordinal >= binaryLength:
                break
        # check if we have reached the end of the message break outer loop
        if ordinal >= binaryLength:
            break
        j = 0


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


"""
    get_binary_string
    This function takes a string and converts it to a binary string. Each character
    in the string is converted to its ASCII value, and then to an 8-bit binary string.
    The binary strings are concatenated together to form a single binary string.

    Args:
        message: String to convert to binary
    Returns:
        binaryMessage: String, binary representation of the input string
"""
def get_binary_string(message: str) -> str:
    # declarations
    binaryMessage = ""
    binaryChar = ""
    intChar = 0

    for char in message:
        # convert char to int
        intChar = ord(char)
        # converts char to 8 bit binary string
        binaryChar = format(intChar, f'0{CHAR_SIZE_BITS}b') 
        # append binaryChar to binaryMessage
        binaryMessage += binaryChar

    return binaryMessage    


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
            # Each pixel has 3 channels (R,G,B), and we use 1 bit per channel
            imageCapacity = ((width * height * 3) - HEADER_SIZE_BITS) // 8  # Convert to bytes
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
            print(f"Message is too long. Maximum capacity is {imageCapacity} bytes (image has {width}x{height} pixels).")
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
            return retrieve_message(img)
        case _:
            # I don't know how it could get here, just covering my bases
            print(f"Error in option") 
            return EXIT_CODE.GENERAL_ERROR

    return EXIT_CODE.SUCCESS

if __name__ == "__main__":
    sys.exit(main())
