import auto_palette
import cv2
import numpy

# os.rename("spidey.png", "spidey1.txt")


# Note that black color aka (ffffff) is recognized as a blank pixel in png files. Therefore, the program does not have the ability to modify absolute black pixels.


imageA = cv2.imread("spidey.png", cv2.IMREAD_UNCHANGED)
print(imageA.shape)
print(type(imageA))

pixel = imageA[8, -8]  # which gives the value 255 155 99
print(pixel)  # B   G   R
print(type(pixel))
print(pixel[0])
print(pixel[1])
print(pixel[2])
print(pixel == 0)

#cv2.imwrite('img.png', imageA)


auto_palette.print_image(imageA)


