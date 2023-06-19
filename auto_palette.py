import tkinter
from tkinter import *
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


def display_palettes(*palettes):
    window = Tk()
    window.title("Palette Display")

    # should add a sorting algorithm to display colors aligned with corresponding color matches on other palettes
    # this sorting should be executed only when each input palette is in equal size

    # should add conditions that checks unordinary arguments such as no argument or image inputs
    # -if no arguments passed- then -create the window with no pre-made palette, so the users are going to create one themselves on gui-

    # defining functions for the mouse behaviour

    def drag_start(event):
        widget = event.widget
        print(widget)
        if isinstance(widget, Label):
            start = (event.x, event.y)
            grid_info = widget.grid_info()
            widget.bind("<B1-Motion>", lambda motion_event: drag_motion(motion_event, widget, start))
            widget.bind("<ButtonRelease-1>", lambda end_event: drag_end(end_event, widget, grid_info))
        else:
            window.unbind("<ButtonRelease-1>")

    def drag_motion(event, widget, start):
        x = widget.winfo_x() + event.x - start[0]
        y = widget.winfo_y() + event.y - start[1]
        widget.lift()
        widget.place(x=x, y=y)

    def drag_end(event, widget, grid_info):
        widget.lower()
        x, y = window.winfo_pointerxy()
        target_widget = window.winfo_containing(x, y)
        if isinstance(target_widget, Label):
            target_grid = target_widget.grid_info()
            if target_widget.cget("text") == "<--->":
                # decide whether it is going to place the color to the right or to the left

                # shift all left labels to the right
                color_to_right = target_grid['column']+1
                while window.grid_slaves(target_grid['row'], color_to_right) is Label and window.grid_slaves(target_grid['row'], color_to_right).cget('bg') is not None:
                    pass
                # place the dropped Label
                widget.grid(row=target_grid['row'], column=target_grid['column']+1)
            elif target_widget.cget("text") == "|\n⌄":
                pass
            else:
                # target & dropped label switch place
                target_widget.grid(row=grid_info['row'], column=grid_info['column'])
                widget.grid(row=target_grid['row'], column=target_grid['column'])
        else:
            widget.grid(row=grid_info['row'], column=grid_info['column'])

    # constructing gui window

    palette_row = 0
    for palette in range(len(palettes)):
        palette_row = (palette + 1) * 2
        Label(window, text="Palette {}".format(palette_row + 1)).grid(row=palette_row * 2, column=0, sticky=S, pady=2)
        for color_row in range(palettes[palette].size):
            stack_label = Label(window, text="|\n⌄", width=15, height=2)
            stack_label.grid(row=palette_row * 2 - 1, column=2 * color_row + 1)
            color_widget = Label(window, background=palettes[palette].colors[color_row], width=6, height=3, text='',
                                 anchor='sw')
            color_widget.grid(row=palette_row * 2, column=2 * color_row + 1, pady=5, padx=5, sticky=N + S + W + E)
            color_widget.bind("<Button-1>", drag_start)
            hex_value = Text(window, width=15, height=1)
            hex_value.grid(row=(palette_row * 2) + 1, column=2 * color_row + 1, sticky=W, pady=2)
            hex_value.insert(INSERT, "#")

            if color_row < palettes[palette].size - 1:
                Label(window, text="<--->", height=6).grid(row=palette_row * 2, column=2 * color_row + 2)

    window.mainloop()
