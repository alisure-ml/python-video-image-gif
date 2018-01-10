# coding: utf-8
import os
from PIL import Image
import images2gif


# 图片排序
class SortGif:

    # 按照创建时间比较
    @staticmethod
    def compare_ctime(x, y):
        if os.stat(x).st_ctime < os.stat(y).st_ctime:
            return -1
        return 1

    # 按照修改时间比较
    @staticmethod
    def compare_mtime(x, y):
        if os.stat(x).st_mtime < os.stat(y).st_mtime:
            return -1
        return 1

    pass


class ToolGif:

    # 初始化
    def __init__(self, source_dir, gif_name, sort=SortGif.compare_mtime, repeat=True, duration=0.2):
        self.__source_dir = source_dir
        self.__gif_name = gif_name
        self.__repeat = repeat
        self.__duration = duration
        self.__sort = sort

        # 生成Gif
        self.__images_to_gif()

        pass

    # 生成Gif
    def __images_to_gif(self):
        # 获取需要放到gif中的文件
        full_img_files = []
        _img_files = os.listdir(self.__source_dir)
        for key in _img_files:
            full_img_files.append(self.__source_dir + key)

        # 按照排序规则进行排序
        full_img_files.sort(self.__sort)

        # 读取图片
        imgs = []
        for img_file in full_img_files:
            imgs.append(Image.open(img_file))

        # 写入Gif
        images2gif.writeGif(self.__gif_name, imgs, repeat=self.__repeat, duration=self.__duration)

        pass


if __name__ == "__main__":

    img_dir = "test/img/"
    gif_dir = "test/gif/test.gif"

    ToolGif(img_dir, gif_dir, sort=SortGif.compare_mtime, duration=0.2)

    pass