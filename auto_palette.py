import numpy


class Palette:
    def __init__(self, *input_colors):

        def check_hex(string) -> bool:
            for char in string:
                if (char < '0' or char > '9') and (char < 'A' or char > 'F') and (char < 'a' or char > 'f'):
                    return False
            return True

        def rgb_to_hex(rgb):
            for value in rgb:
                if value < 0 or value > 255:
                    raise TypeError("only RGB values that are between 0 and 255 are accepted")
            return '#%02x%02x%02x' % rgb

        formatted_colors = []

        for color in input_colors:
            if type(color) is tuple:
                if len(color) == 3:
                    formatted_colors.append(rgb_to_hex(color))
                    continue
                elif len(color) == 4:
                    color = color[0:3]
                    formatted_colors.append(rgb_to_hex(color))
                    continue
                else:
                    raise ValueError(
                        "RGB color value is not properly formatted at {}th index".format(input_colors.index(color)))
            elif type(color) is str:
                for piece in color.split():
                    if (len(piece) == 4 or len(piece) == 7) and piece.startswith('#') and check_hex(
                            piece.removeprefix('#')):
                        formatted_colors.append(piece)
                        continue
                    elif (len(piece) == 3 or len(piece) == 6) and check_hex(piece):
                        piece = '#' + piece
                        formatted_colors.append(piece)
                        continue
                    else:
                        raise ValueError(
                            "hex color value is not properly formatted at {}th index".format(input_colors.index(color)))

        # should add here a sorting algorithm for colors to have similar colors side by side (likes shades or contrasts)

        self.colors = formatted_colors
        self.size = len(formatted_colors)


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
    Trims the png image with relatively less 4 channel value pixels based on the given tolerance value from 0 (being 
    least tolerant) to 255 (being most tolerant) 
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

    # should add here a sorting algorithm for colors to have similar colors side by side (likes shades or contrasts)

    return str_palette


def color_into_hexcode(colorRGB) -> str:
    hexcode = "#"
    for value in colorRGB:
        hexcode += str(hex(value)).removeprefix("0x")
    return hexcode
