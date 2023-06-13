import cv2
import numpy

def print_image(image):
    for column in range(len(image)):
        for row in range(len(image)):
            if image[column, row].all() == 0:
                print("-", end='')
            else:
                print("#", end='')
        print("\n")


# Note that it does not insert the input
def flipped_horizontally(image) -> numpy.ndarray:
    flipped_image = numpy.zeros((len(image), len(image[0]), 4), dtype=numpy.uint8)
    for row in range(len(image)):
        for column in range(len(image[row])):
            new_column = -column - 1
            flipped_image[row, new_column] = image[row, column]
    return flipped_image


# Note that it does not insert the input
def flipped_vertically(image) -> numpy.ndarray:
    flipped_image = numpy.zeros((len(image), len(image[0]), 4), dtype=numpy.uint8)
    for row in range(len(image)):
        new_row = -row - 1
        for column in range(len(image[row])):
            flipped_image[new_row, column] = image[row, column]
        print("\n")
    return flipped_image


# Note that it inserts the input
def trim_channel4(image, tolerance):
    """
    Trims the png image with relatively less 4 channel value pixels based on the given tolerance value from 0 (being least tolerant) to 255 (being most tolerant)
    """

    if not type(tolerance) is int:
        raise TypeError("Only tolerance value can only be integers")

    if tolerance < 0 or tolerance > 255:
        raise Exception("Tolerance value can be from 0 up to 255. Please enter a number within that range")

    for row in range(len(image)):
        for column in range(len(image[row])):
            pixel = image[row, column]
            if pixel[3] >= tolerance:
                pixel[4] = 255


def extract_palette(image):
    # extracting all colors, also removing black & whites for the set if there are one
    colors = set()
    for row in range(len(image)):
        for column in range(len(image[row])):
            colorRGB = (image[row, column][2], image[row, column][1], image[row, column][0])
            if colorRGB == (0, 0, 0) or colorRGB == (255, 255, 255):
                continue

            if colorRGB not in colors:
                colors.add(colorRGB)

    # preparing string to output
    str_palette = str()
    for colorRGB in colors:
        str_palette += color_into_hexcode(colorRGB) + " "

    return str_palette


def color_into_hexcode(colorRGB) -> str:
    hexcode = "#"
    for value in colorRGB:
        hexcode += str(hex(value)).removeprefix("0x")
    return hexcode
