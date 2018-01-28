import numpy as np
from glob import glob
from PIL import Image
from datetime import datetime
import matplotlib.pyplot as plt


# 读取图像
def read_image(image_path):
    return np.array(Image.open(image_path))


def show_video(image_names, mask_names, mask_color=list([255, 0, 0]), opacity=0.5):
    # 打开交互模式
    plt.ion()
    for image_key, image_name in enumerate(image_names):
        print("{} {}".format(image_key, datetime.now()))
        # 读取图片
        image = read_image(image_name)
        mask = read_image(mask_names[image_key])
        mask = mask / np.max(mask)
        # 新建图片数组
        image_mask = np.ndarray(image.shape)
        # 进行mask
        image_mask[:, :, 0] = (1 - mask) * image[:, :, 0] + mask * (opacity * mask_color[0] + (1 - opacity) * image[:, :, 0])
        image_mask[:, :, 1] = (1 - mask) * image[:, :, 1] + mask * (opacity * mask_color[1] + (1 - opacity) * image[:, :, 1])
        image_mask[:, :, 2] = (1 - mask) * image[:, :, 2] + mask * (opacity * mask_color[2] + (1 - opacity) * image[:, :, 2])
        # 显示图片
        plt.imshow(image_mask.astype(np.uint8))
        # 关闭坐标轴
        plt.axis('off')
        # 暂停
        plt.pause(0.01)
        # 清除目前的图像
        plt.clf()
    pass

if __name__ == '__main__':

    """
    速度非常的慢，建议直接使用OpenCV
    """

    show_video(sorted(glob("bear/bottom/*")), sorted(glob("bear/top/*")))

    pass
