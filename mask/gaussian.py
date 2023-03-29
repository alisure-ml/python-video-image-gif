import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter, ImageEnhance  

def _mask_gaussian(data_xy, where, ellipse_size=list([1.0, 1.0]), sigma=30):
      x = np.arange(0, data_xy[1], 1, float) * ellipse_size[0]
      y = np.arange(0, data_xy[0], 1, float) * ellipse_size[1]
      y = y[:, np.newaxis]

      x0 = where[1]
      y0 = where[0]

      # 生成高斯掩码
      mask = np.exp(-4 * np.log(2) * ((x - x0 * ellipse_size[0]) ** 2 +
                                      (y - y0 * ellipse_size[1]) ** 2) / sigma ** 2).astype(np.float32)
      # mask[mask < 0.5] = 0.5
      mask = mask + 1.0
      return mask


