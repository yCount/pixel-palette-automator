import numpy


class Color:
    def __init__(self, R, G, B):
        self.color_code = (R, G, B)

    def name(self):
        # should name colors through hashing based on the self.color_value
        pass


class Palette:
    def __init__(self, *input_colors):
        # should add here a sorting algorithm for colors to have similar colors side by side (likes shades or contrasts)

        self.colors = list(input_colors)

    def color_switch_place(self, index, target_index):
        target_color = self.colors[target_index]
        self.colors[target_index] = self.colors[index]
        self.colors[index] = target_color

    def color_change_placement(self, index, target_edge):

        # The number should be rolled to be bigger int if color's index is larger and if smaller then smaller

        moved_color = self.colors.pop(index)

        self.colors.insert(target_edge, moved_color)

    def pair_colors(self, index, target_index):
        self.colors[target_index].insert(0, self.colors[index])
        (index, target_index)


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


def extract_palette(image):
    # extracting all colors, also removing black & whites for the set if there are one
    seen_colors = set()
    for row in range(len(image)):
        for column in range(len(image[row])):
            colorRGB = (image[row, column][2], image[row, column][1], image[row, column][0])
            if colorRGB == (0, 0, 0) or colorRGB == (255, 255, 255):
                continue

            if colorRGB not in seen_colors:
                seen_colors.add(colorRGB)

    # should add here a sorting algorithm for colors to have similar colors side by side (likes shades or contrasts)
    palette = Palette(seen_colors)
    return palette
