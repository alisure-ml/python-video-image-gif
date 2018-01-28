import os
import csv
import cv2
import random
from datetime import datetime


# 读取信息
def read_annotations_from_csv(csv_file_name):
    with open(csv_file_name, "r") as f:
        rows = []
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    return rows


def video_from_ava(video_filename, annotations_filename, result_path):

    # 结果目录
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # capture the video
    cap = cv2.VideoCapture(video_filename)

    # 获取帧的信息
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    speed_frame = int(cap.get(cv2.CAP_PROP_FPS))

    print("frames width {}".format(width))
    print("frames height {}".format(height))
    print("frames number {}".format(total_frame))
    print("frames speed {}".format(speed_frame))

    # 读取注解
    video_annotations = read_annotations_from_csv(annotations_filename)

    for i,video_annotation in enumerate(video_annotations):
        # 开始的帧和结束的帧
        start_frame = int(video_annotation[1]) * speed_frame
        end_frame = (int(video_annotation[1]) + 3) * speed_frame

        # 设置开始的帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        is_break = False

        # 存储帧
        video_frames = []

        # 读取图片信息
        for _ in range(start_frame, end_frame):
            # read a frame
            ret, image = cap.read()

            if ret:
                video_frames.append(image)

                # exit if Escape is hit
                if cv2.waitKey(10) == 27:
                    is_break = True
                    break
            else:
                raise Exception("执行中发生错误")
            pass

        # 保存视频
        images_to_video(video_frames, speed_frame,
                        "{}/{}_{}_{}_{}.mp4".format(result_path, video_annotation[1],
                                                    video_annotation[6], len(video_frames), random.randint(0, 1000)))

        if i % 1 == 0:
            print("{} {}/{}/{}".format(datetime.now(), i, video_annotation[1], len(video_annotations)))
            pass

        # 跳出
        if is_break:
            break
        pass

    cv2.destroyAllWindows()
    cap.release()
    print("Done")
    pass


def images_to_video(video_frames, speed_frame, result_filename):
    if len(video_frames) <= 0:
        raise Exception("zz")

    # initiate the video with width, height and pfs
    height, width, _ = video_frames[0].shape
    four_cc = cv2.VideoWriter_fourcc(*"mp4v")  # mp4
    video = cv2.VideoWriter(result_filename, four_cc, speed_frame, (width, height))

    # 将图片写入视频
    for video_frame in video_frames:
        video.write(video_frame)

    cv2.destroyAllWindows()
    video.release()
    pass


if __name__ == "__main__":
    video_from_ava(video_filename="data/zR725veL-DI.mp4",
                   annotations_filename="data/ava_test_v1.0.csv",
                   result_path="result/zR725veL-DI")
