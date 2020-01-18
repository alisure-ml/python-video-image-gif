"""
从监控视频中剪切出感兴趣的部分
"""

import os
from ToolVideo import crop_video
from alisuretool.Tools import Tools

# input_path = "/home/ubuntu/data1.5TB/video/video_deal/show"
# result_path = Tools.new_dir("/home/ubuntu/data1.5TB/video/video_deal/sketch_flow_2/video")
# video_info = [
#     [os.path.join(input_path, "20180707_20180707091950_20180707092036_092247.avi"), [250, 50, 550, 350]],
#     [os.path.join(input_path, "20181009_20181009090613_20181009090627_090339.avi"), [160, 240, 360, 440]],
#     [os.path.join(input_path, "20180707_20180707091950_20180707092036_092247.avi"), [400, 200, 900, 700]],
# ]

# input_path = "/home/ubuntu/data1.5TB/video/video_deal/show"
# result_path = Tools.new_dir("/home/ubuntu/data1.5TB/video/video_deal/sketch_flow_2/video")
# video_info = [
#     [os.path.join(input_path, "20180707_20180707091950_20180707092036_092247.avi"),
#      [1080//2-200, 720//2-150, 1080//2+400, 720//2+250]],
# ]

# input_path = "/home/ubuntu/data1.5TB/video/video_deal/sketch_flow_2/select_video/20180523_20180523155357_20180523174805_155633"
# result_path = Tools.new_dir("/home/ubuntu/data1.5TB/video/video_deal/sketch_flow_2/video")
# video_info = [[os.path.join(input_path, "1740_1748.avi"),
#                [704//2-350, 576//2-133, 704//2+150, 576//2+200]]]
# video_info = [[os.path.join(input_path, "2295_2300.avi"),
#                [704//2-350, 576//2-100, 704//2+150, 576//2+233]]]
# video_info = [[os.path.join(input_path, "3817_3835.avi"),
#                [704//2-350, 576//2-150, 704//2+250, 576//2+250]]]

# input_path = "/home/ubuntu/data1.5TB/video/video_deal/sketch_flow_2/select_video/20180707_20180707092133_20180707093648_092428"
# result_path = Tools.new_dir("/home/ubuntu/data1.5TB/video/video_deal/sketch_flow_2/video")
# video_info = [[os.path.join(input_path, "0_4.avi"),
#                [704//2-100, 576//2-110, 704//2+200, 576//2+90]]]

input_path = "/home/ubuntu/data1.5TB/video/video_deal/sketch_flow_2/select_video"
result_path = Tools.new_dir("/home/ubuntu/data1.5TB/video/video_deal/sketch_flow_2/video")
# video_info = [[os.path.join(input_path, "01_0053电动三轮车_5_8.avi"),
#                [856//2-380, 480//2-210, 856//2+100, 480//2+150]]]
# video_info = [[os.path.join(input_path, "10_0074摩托车_20_23.avi"),
#                [856//2-420, 480//2-110, 856//2+90, 480//2+230]]]
# video_info = [[os.path.join(input_path, "05_0019聚众推搡_7_13.avi"),
#                [856//2-420, 480//2-190, 856//2+90, 480//2+150]]]
# video_info = [[os.path.join(input_path, "05_043_15_23.avi"),
#                [856//2-90, 480//2-190, 856//2+420, 480//2+170]]]
video_info = [[os.path.join(input_path, "08_020_5_20.avi"),
               [856//2-420, 480//2-180, 856//2+120, 480//2+200]]]

for video_one in video_info:
    input_filename = os.path.splitext(os.path.basename(video_one[0]))[0]
    result_filepath = os.path.join(result_path, "{}_{}_{}_{}_{}.avi".format(
        input_filename, video_one[1][0], video_one[1][1], video_one[1][2], video_one[1][3]))
    crop_video(video_one[0], result_filepath, video_one[1])
    pass

