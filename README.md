# Homework 3: Steganography

Matthew J. Martin
CS-465-001 SP 24-25
Assignment 3
Due: 25 May 2025

## Requirements

### 1. Hiding a Message:
- Implement functionality to hide a text message within an image using LSB steganography.
- Your program should take the following inputs:
  - An option (`"hide"`).
  - The image name of the original cover image (e.g., `"cover.png"`).
  - The message to hide.
  - The program should output a new image file (e.g., `"cover_new.png"`) containing the hidden message.

### 2. Retrieving a Message:
- Implement functionality to retrieve the hidden message from the modified image.
- Your program should take the following inputs:
  - An option (`"retrieve"`).
  - The name of the image containing the hidden message (e.g., `"cover_new.png"`).
- The program should output the hidden message in plain text.

## Example

**Hiding a Message:**
```
python imageLSB.py hide cover.png "This is a random message!"
```
- Output: cover_new.png

**Retrieving a Message:**
```
python imageLSB.py retrieve cover_new.png
```
- Output: "This is a random message!"

## Submission Instructions

- **Code Submission:** Submit your code file (`imageLSB.py`).
- **Build/Run Instructions:** Include a README file with any necessary instructions for building, compiling, and running your code. Keep the instructions simple and clear.

## Notes

- The new image (`cover_new.jpg`) should be indistinguishable from the original cover image (`cover.jpg`) to the human eye, as LSB steganography does not alter the image perceptibly.
- Ensure that the program automatically retrieves the entire message without needing additional parameters.
