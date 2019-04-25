import numpy as np
from PIL import Image


def read_image(image_path):
    return Image.open(image_path).convert("RGB")


def show_image(im_or_array):
    if isinstance(im_or_array, np.ndarray):
        Image.fromarray(im_or_array).convert("RGB").show()
    else:
        im_or_array.show()
    pass


def resize_image(im, resize):
    return im.resize(resize)


if __name__ == '__main__':
    cell_width = 80
    cell_height = 80
    cell_padding = 5
    col_number = 6
    row_number = 4

    image_path = [
        [0,
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg"],
        ["/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg"],
        ["/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg"],
        ["/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg",
         "/home/ubuntu/PycharmProjects/ALISURE/python-video-image-gif/draw_image/data/zs_ft/image/n02121620_32013.jpg"]
    ]

    image_width = cell_width * col_number + cell_padding * (col_number + 1)
    image_height = cell_height * row_number + cell_padding * (row_number + 1)

    im = Image.fromarray(np.zeros(shape=[image_height, image_width, 3], dtype=np.uint8) + 248).convert("RGB")
    for i in range(row_number):
        for j in range(col_number):
            now_path = image_path[i][j]
            if now_path == 0:
                continue
            im2 = read_image(now_path)
            im2 = resize_image(im2, [cell_width, cell_height])
            x1 = j * cell_width + (j + 1) * cell_padding
            y1 = i * cell_height + (i + 1) * cell_padding
            im.paste(im2, (x1, y1, x1 + cell_width, y1 + cell_height))
            pass
        pass

    show_image(im)

    pass
