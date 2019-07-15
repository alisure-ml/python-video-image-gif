"""
从监控视频中剪切出感兴趣的部分
"""

import os
from ToolVideo import crop_video
from alisuretool.Tools import Tools

input_path = "/home/ubuntu/data1.5TB/video/video_deal/show"
result_path = Tools.new_dir("/home/ubuntu/data1.5TB/video/video_deal/sketch_flow/video")

video_info = [
    [os.path.join(input_path, "20180707_20180707091950_20180707092036_092247.avi"), [250, 50, 550, 350]],
    [os.path.join(input_path, "20181009_20181009090613_20181009090627_090339.avi"), [160, 240, 360, 440]],
    [os.path.join(input_path, "20180707_20180707091950_20180707092036_092247.avi"), [400, 200, 900, 700]],
]

for video_one in video_info:
    input_filename = os.path.splitext(os.path.basename(video_one[0]))[0]
    result_filepath = os.path.join(result_path, "{}_{}_{}_{}_{}.avi".format(
        input_filename, video_one[1][0], video_one[1][1], video_one[1][2], video_one[1][3]))
    crop_video(video_one[0], result_filepath, video_one[1])
    pass

