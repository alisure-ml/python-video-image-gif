"""
将视频转化为图片数据
"""

import os
import cv2
from alisuretool.Tools import Tools
from ToolVideo import video_to_images, images_to_video, video_to_images_to_video

input_path = "/home/ubuntu/data1.5TB/video/video_deal/sketch_flow/video"
result_path = Tools.new_dir("/home/ubuntu/data1.5TB/video/video_deal/sketch_flow/image")

video_file_path = [os.path.join(input_path, video_file) for video_file in os.listdir(input_path)]

for video_file in video_file_path:
    image_path = Tools.new_dir(os.path.join(result_path, os.path.splitext(os.path.basename(video_file))[0]))
    video_to_images(video_file, result_path=image_path)
    pass

