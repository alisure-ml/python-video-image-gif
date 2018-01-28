import os
import csv
import cv2
import random
import pickle
import numpy as np
from datetime import datetime


class AVA(object):

    def __init__(self, annotations_filename, video_filename, result_path,
                 action_list_file="data/ava_action_list_v1.0.pkl"):

        # 读取注解
        self.video_annotations = self._read_annotations_from_csv(annotations_filename)

        # 行为名称
        self.action_list_file = action_list_file
        if not os.path.exists(self.action_list_file):
            self.__read_name_from_pbtxt()
        self.action_list = self._get_action_names(action_list_file)

        # 视频
        self.video_filename = video_filename

        # 结果目录
        self.result_path = result_path
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
            pass

        # capture the video
        self.cap = cv2.VideoCapture(self.video_filename)

        # 获取帧的信息
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frame = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.speed_frame = int(self.cap.get(cv2.CAP_PROP_FPS))

        pass

    # 读取annotation信息
    @staticmethod
    def _read_annotations_from_csv(csv_file_name):
        with open(csv_file_name, "r") as f:
            rows = []
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)
        return rows

    # 增加mask
    def _add_mask_in_image(self, image, left_top, bottom_right, action_id):
        mask = np.zeros_like(image)

        # 画矩形
        cv2.rectangle(mask, (left_top[0], left_top[1]), (bottom_right[0], bottom_right[1]), (0, 0, 255), thickness=2)
        # 写字
        cv2.putText(image, self._get_action_name_by_id(action_id), org=(left_top[0] + 10, left_top[1] + 30),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)

        image = cv2.add(image, mask)
        return image

    # 解析ava视频
    def _video_from_ava(self):
        # 开始解析
        for i, video_annotation in enumerate(self.video_annotations):
            is_break = False

            # 解析
            middle_time = float(video_annotation[1])
            action_id = video_annotation[6]

            # 开始的帧和结束的帧,中间帧+-1.5S
            start_frame = int((middle_time - 1.5) * self.speed_frame)
            start_mask_frame = int((middle_time - 0.5) * self.speed_frame)
            end_mask_frame = int((middle_time + 0.5) * self.speed_frame)
            end_frame = int((middle_time + 1.5) * self.speed_frame)
            # 设置开始的帧
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

            # 框的边界
            left_top = [int(float(video_annotation[2]) * self.width), int(float(video_annotation[3]) * self.height)]
            bottom_right = [int(float(video_annotation[4]) * self.width), int(float(video_annotation[5]) * self.height)]

            # 存储帧
            video_frames = []
            # 读取图片信息
            for now_frame in range(start_frame, end_frame):
                # read a frame
                ret, image = self.cap.read()
                if ret:
                    # 画框
                    if start_mask_frame < now_frame < end_mask_frame:
                        image = self._add_mask_in_image(image, left_top, bottom_right, action_id)
                    video_frames.append(image)
                    # exit if Escape is hit
                    if cv2.waitKey(10) == 27:
                        is_break = True
                        break
                else:
                    raise Exception("执行中发生错误")
                pass

            # 保存视频
            self._images_to_video(video_frames, "{}/{}_{}_{}_{}.mp4".format(self.result_path, int(middle_time),
                                                                            action_id, len(video_frames),
                                                                            random.randint(0, 1000)))

            # 打印信息
            if i % 1 == 0:
                print("{} {}/{}/{}".format(datetime.now(), i, int(middle_time), len(self.video_annotations)))
                pass
            # 跳出
            if is_break:
                break
            pass

        cv2.destroyAllWindows()
        self.cap.release()
        print("Done")
        pass

    # 图像到视频
    def _images_to_video(self, video_frames, result_filename):
        if len(video_frames) <= 0:
            raise Exception("zz")

        # initiate the video with width, height and pfs
        height, width, _ = video_frames[0].shape
        four_cc = cv2.VideoWriter_fourcc(*"mp4v")  # mp4
        video = cv2.VideoWriter(result_filename, four_cc, self.speed_frame, (width, height))

        # 将图片写入视频
        for video_frame in video_frames:
            video.write(video_frame)

        cv2.destroyAllWindows()
        video.release()
        pass

    # 解析pbtxt,保存成pkl
    @staticmethod
    def __read_name_from_pbtxt(pbtxt_file_name="data/ava_action_list_v1.0.pbtxt"):
        action_list = []
        with open(pbtxt_file_name, "r") as f:
            actions = f.read().replace(" ", "").replace("\n", "").split("}")
            for action in actions:
                if "name" in action and "label_id" in action and "label_type" in action:
                    name = action.split("\"")[1]
                    label_id = action.split("label_id:")[1].split("label")[0]
                    label_type = action.split(":")[-1]
                    action_list.append({"name": name, "label_id": label_id, "label_type": label_type})
            pass
        with open("{}.pkl".format(os.path.splitext(pbtxt_file_name)[0]), "wb") as f:
            pickle.dump(action_list, f)
        pass

    # 根据id得到动作名称
    @staticmethod
    def _get_action_names(action_list_file):
        with open(action_list_file, "rb") as f:
            return pickle.load(f)
        pass

    # 根据id得到动作
    def _get_action_by_id(self, action_id):
        now_action = self.action_list[int(action_id) - 1]
        return int(now_action["label_id"]), now_action["label_type"], now_action["name"]

    # 根据id得到动作名称
    def _get_action_name_by_id(self, action_id):
        now_action = self.action_list[int(action_id) - 1]
        return now_action["name"]

    # run
    def run(self):
        print("wideo width:{},height:{},number:{},speed:{}".format(self.width, self.height,
                                                                   self.total_frame, self.speed_frame))

        self._video_from_ava()
        pass
    pass


if __name__ == "__main__":
    ava = AVA(video_filename="data/zR725veL-DI.mp4",
              annotations_filename="data/ava_test_v1.0.csv",
              result_path="result/zR725veL-DI")
    ava.run()
