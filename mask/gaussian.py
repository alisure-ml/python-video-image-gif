import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter, ImageEnhance


def _mask_gaussian(data_xy, where, ellipse_size=list([1.0, 1.0]), sigma=30):
    x = np.arange(0, data_xy[1], 1, float) * ellipse_size[0]
    y = np.arange(0, data_xy[0], 1, float) * ellipse_size[1]
    y = y[:, np.newaxis]

    x0, y0 = where[1], where[0]

    # 生成高斯掩码
    mask = np.exp(-4 * np.log(2) * ((x - x0 * ellipse_size[0]) ** 2 +
                                    (y - y0 * ellipse_size[1]) ** 2) / sigma ** 2).astype(np.float32)
    return mask


def demo_1():
    mask = _mask_gaussian(data_xy=[32, 32], where=[10, 15], sigma=3)
    im = Image.fromarray(np.asarray(mask * 255, dtype=np.uint8))
    im.show()
    pass


def demo_2():
    where_list = [[10, 15], [15, 15], [16, 16], [20, 24]]
    mask = np.zeros(shape=(32, 32), dtype=float)
    for where in where_list:
        mask += _mask_gaussian(data_xy=[32, 32], where=where, ellipse_size=list([0.8, 0.8]), sigma=4)
    mask[mask>1.0] = 1.0
    im = Image.fromarray(np.asarray(mask * 255, dtype=np.uint8))
    im.show()
    pass
