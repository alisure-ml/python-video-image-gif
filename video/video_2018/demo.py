import os
import cv2
from ToolVideo import video_to_images, images_to_video, video_to_images_to_video, crop_video

video_orig_path = "/home/ubuntu/data1.5TB/video"
video_deal_path = "/home/ubuntu/data1.5TB/video/video_deal"

all_video_orig = [os.path.join(video_orig_path, video_orig)
                  for video_orig in os.listdir(video_orig_path) if ".mp4" in video_orig]


# 得到视频的第一帧
# get_first_frame(all_video_orig)
def get_first_frame(video_list):
    for video_now_name in video_list:
        cap = cv2.VideoCapture(video_now_name)

        print(cap.get(3))
        print(cap.get(4))

        ret, frame = cap.read()
        if ret:
            save_image_path = os.path.join(
                video_deal_path, "first_frame", "{}.jpg".format(os.path.splitext(os.path.basename(video_now_name))[0]))
            cv2.imwrite(save_image_path, frame)
            pass

        cap.release()
        cv2.destroyAllWindows()
        pass
    pass


# 读取视频
# deal_video(all_video_orig[0])
def read_video(video_file_name):
    cap = cv2.VideoCapture(video_file_name)
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(video_file_name)
    print(total_frame)
    print(cap.get(3))
    print(cap.get(4))

    count = 0
    while True:
        ret, frame = cap.read()
        if ret:
            count += 1
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xff == "q":
                break
        else:
            break

    print(count)

    cap.release()
    cv2.destroyAllWindows()

    pass


# 转换视频
# tran_video("/home/ubuntu/data1.5TB/video/20181009_20181009090613_20181009090627_090339.mp4")  # 340, 人群正向
# tran_video("/home/ubuntu/data1.5TB/video/20181009_20181009090556_20181009090638_090323.mp4")  # 1037, 人群逆向，电动车
# tran_video("/home/ubuntu/data1.5TB/video/20180707_20180707091950_20180707092036_092247.mp4")  # 772, 人群正逆向，汽车
# tran_video("/home/ubuntu/data1.5TB/video/20180707_20180707091813_20180707091839_092109.mp4")  # 257, 人群正逆向，汽车
# tran_video("/home/ubuntu/data1.5TB/video/20180618_20180618130144_20180618130153_130434.mp4")  # 216, 人群逆向，下雨
# tran_video("/home/ubuntu/data1.5TB/video/20180618_20180618104346_20180618104405_104642.mp4")  # 482, 人群正向，下雨，汽车
# tran_video("/home/ubuntu/data1.5TB/video/20180526_20180526164312_20180526164416_164552.mp4")  # 1608, 人群逆向
# tran_video("/home/ubuntu/data1.5TB/video/20180526_20180526164305_20180526164322_164544.mp4")  # 437, 人群逆向，汽车
# tran_video("/home/ubuntu/data1.5TB/video/20180525_20180525201133_20180525201347_201410.mp4")  # 1888(裁剪), 夜晚暗，人群逆向，动物
# tran_video("/home/ubuntu/data1.5TB/video/20180525_20180525200344_20180525200605_200621.mp4")  # 3518, 夜晚亮，人群正逆向
# tran_video("/home/ubuntu/data1.5TB/video/21_12_14.mp4")  # 1471, 走廊，人群正逆向
def tran_video(video_file_name):
    image_path = os.path.join(video_deal_path, "tran", os.path.splitext(os.path.basename(video_file_name))[0])
    images, count = video_to_images(video_file_name, is_save=False, result_path=image_path)
    images_to_video(image_path, 0, count, rep=1, images=images)
    pass


# tran_video("/home/ubuntu/data1.5TB/video/20180707_20180707095304_20180707103348_095601.mp4")  # 40:44, 校门口
# tran_video("/home/ubuntu/data1.5TB/video/20180707_20180707092133_20180707093648_092428.mp4")  # 15:15, 校门口
# tran_video("/home/ubuntu/data1.5TB/video/20180523_20180523155417_20180523174808_155653.mp4")  # 没有人，只有背景
# tran_video("/home/ubuntu/data1.5TB/video/20180523_20180523155402_20180523174814_155638.mp4")  #
# tran_video("/home/ubuntu/data1.5TB/video/20180523_20180523155357_20180523174805_155633.mp4")  #
# tran_video("/home/ubuntu/data1.5TB/video/20180523_20180523155354_20180523174807_155631.mp4")  #
# tran_video("/home/ubuntu/data1.5TB/video/20180523_20180523155352_20180523174812_155628.mp4")  #
# tran_video("/home/ubuntu/data1.5TB/video/20180523_20180523155351_20180523174813_155627.mp4")  #
# tran_video("/home/ubuntu/data1.5TB/video/20180522_20180522164114_20180522175049_164352.mp4")  #
# tran_video("/home/ubuntu/data1.5TB/video/20180522_20180522164111_20180522175048_164349.mp4")  #
# tran_video("/home/ubuntu/data1.5TB/video/20180522_20180522164108_20180522175043_164346.mp4")  #
# tran_video("/home/ubuntu/data1.5TB/video/20180522_20180522164106_20180522175051_164345.mp4")  # 3300
# tran_video("/home/ubuntu/data1.5TB/video/20180522_20180522164105_20180522175039_164343.mp4")  #
# tran_video("/home/ubuntu/data1.5TB/video/20180522_20180522164102_20180522175038_164342.mp4")  #
def tran_video_long(video_file_name):
    image_path = os.path.join(video_deal_path, "long", os.path.basename(video_file_name))
    count = video_to_images_to_video(video_file_name, result_filename=image_path)
    pass


# video_to_image("/media/ubuntu/数据/show/video", "/media/ubuntu/数据/show/image")
# video_to_image("/home/ubuntu/data1.5TB/video/video_deal/show", "/home/ubuntu/data1.5TB/video/video_deal/show2")
def video_to_image(video_dir, result_dir):
    video_file_names = [os.path.join(video_dir, file_name) for file_name in os.listdir(video_dir)]
    for file_name in video_file_names:
        video_to_images(file_name,
                        result_path=os.path.join(result_dir, os.path.splitext(os.path.basename(file_name))[0]))
    pass


# crop_video("/home/ubuntu/data1.5TB/video/video_deal/show/20180707_20180707091950_20180707092036_092247.avi",
#                "/home/ubuntu/data1.5TB/video/video_deal/show/20180707_20180707091950_20180707092036_092247_crop.avi",
#                crop_area=list([250, 50, 600, 400]))
def video_crop(video_path, crop_result_video, crop_area):
    crop_video(video_path, crop_result_video, crop_area)
    pass

if __name__ == '__main__':
    images_to_video("/home/ubuntu/data1.5TB/video/video_deal/face/20181009_20181009090613_20181009090627_090339", 0, 339, rep=1)
    pass
