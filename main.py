import auto_palette
import cv2
import numpy



# Note that black color (ffffff in hex) is recognized as a blank pixel in png files. Therefore, the program does not have the ability to modify absolute black pixels.


imageA = cv2.imread("spidey.png", cv2.IMREAD_UNCHANGED)


auto_palette.print_image(imageA)
