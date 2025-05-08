# Homework 3: Steganography

Matthew J. Martin \
CS-465-001 SP 24-25 \
Assignment 3 \
Due: 25 May 2025

## Dependencies:
- Python 3.x
- pillow (PIL) library for image processing (This is installed on Drexel's tux)
- sys module for command line arguments
- os module for file path manipulation

## Assumptions:
- all images are `.png` type images
- hidden message is made entirely of **ASCII** characters

## Usage:
### Hiding:
`python3 imageLBS.py hide <input image> <message>`
### Retrieving:
`python3 imageLBS.py retrieve <input image>`

