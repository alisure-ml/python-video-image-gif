import cv2
from PIL import Image
import numpy as np
import scipy.misc as misc


# Image to cv2
def image_to_cv2():
    image = Image.open("demo.png")
    image.show()

    image = np.array(image)

    img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.imshow("openCV", img)

    cv2.waitKey()
    pass


# misc to cv2
def misc_to_cv2():
    image = misc.imread("demo.png")

    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow("openCV", img)

    cv2.waitKey()
    pass


# Image to misc to cv2
def image_to_misc_to_cv2():
    image_data = np.array(Image.open("demo.png"))

    palette = np.load('palette.npy').tolist()
    draw_palette = Image.fromarray(image_data, 'P')
    draw_palette.putpalette(palette)
    image_b = misc.fromimage(draw_palette)

    img = cv2.cvtColor(image_b, cv2.COLOR_RGB2BGR)
    cv2.imshow("openCV", img)

    cv2.waitKey()
    pass

if __name__ == '__main__':
    image_to_misc_to_cv2()
