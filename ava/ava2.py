import os
import csv
import cv2
import pickle
import numpy as np
from datetime import datetime


class AVA(object):

    def __init__(self, annotations_filename, video_filename, result_path,
                 action_list_file="data/ava_action_list_v1.0.pkl"):

        # 读取注解
        self.video_annotations = self._read_annotations_from_csv(annotations_filename)
        # 合并注解
        self.video_annotations = self._deal_annotations()

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

    # 处理注解：和并
    def _deal_annotations(self):
        # 同一时间多个动作
        now_time = 0
        video_annotations = []
        now_annotations = []
        for annotation in self.video_annotations:
            if now_time != int(annotation[1]):
                now_time = int(annotation[1])
                if len(now_annotations) > 0:
                    video_annotations.append(now_annotations)
                    now_annotations = []
                pass
            now_annotations.append(annotation)
            pass
        # 将最后一个保存
        if len(now_annotations) > 0:
            video_annotations.append(now_annotations)
            pass

        # 同一时间同一目标的多个动作
        video_annotations2 = []
        for annotations in video_annotations:
            # 存放合并后的注解框
            now_annotations2 = []
            point = None
            label_id = []
            now_annotation = []
            for annotation in annotations:
                # 需要检测的值
                tem_point = "{}{}{}{}".format(annotation[2], annotation[3], annotation[4], annotation[5])
                if point is None or point not in tem_point:  # 新的注解框
                    point = tem_point
                    if len(label_id) > 0:  # 保存合并后的注解框
                        now_annotation.append(label_id)
                        now_annotations2.append(now_annotation)
                        label_id = []
                    pass
                # 合并label_id
                label_id.append(annotation[6])
                # 此时的注解框
                now_annotation = annotation[:-1]
                pass
            # 将最后一个保存
            if len(label_id) > 0:  # 保存合并后的注解框
                now_annotation.append(label_id)
                now_annotations2.append(now_annotation)
            video_annotations2.append(now_annotations2)
            pass
        return video_annotations2

    # 增加masks
    def _add_masks_in_image(self, image, left_tops, bottom_rights, action_ids):
        mask = np.zeros_like(image)

        # 画矩形
        for index in range(len(left_tops)):
            cv2.rectangle(mask, (left_tops[index][0], left_tops[index][1]),
                          (bottom_rights[index][0], bottom_rights[index][1]), (0, 0, 255), thickness=2)
            # 写字
            action_names = [self._get_action_name_by_id(action_id) for action_id in action_ids[index]]
            cv2.putText(image, "|".join(action_names), org=(left_tops[index][0] + 10, left_tops[index][1] + 30),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)
            pass

        image = cv2.add(image, mask)
        return image

    # 解析ava视频
    def _video_from_ava(self, is_all_time=True):
        # 大视频 1
        large_video = cv2.VideoWriter("{}/{}.mp4".format(self.result_path, "all"), cv2.VideoWriter_fourcc(*"mp4v"),
                                      self.speed_frame, (self.width, self.height))

        # 开始解析
        for i, now_video_annotations in enumerate(self.video_annotations):
            is_break = False

            # 解析
            middle_time = float(now_video_annotations[0][1])

            # 开始的帧和结束的帧,中间帧+-1.5S
            start_frame = int((middle_time - 1.5) * self.speed_frame)
            end_frame = int((middle_time + 1.5) * self.speed_frame)
            # 设置开始的帧
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            # 设置标注的帧
            if is_all_time:
                start_mask_frame = start_frame
                end_mask_frame = end_frame
            else:
                start_mask_frame = int((middle_time - 0.5) * self.speed_frame)
                end_mask_frame = int((middle_time + 0.5) * self.speed_frame)

            # 框的边界和label
            action_ids = []
            left_tops = []
            bottom_rights = []
            for now_video_annotation in now_video_annotations:
                action_ids.append(now_video_annotation[6])
                left_tops.append([int(float(now_video_annotation[2]) * self.width),
                                  int(float(now_video_annotation[3]) * self.height)])
                bottom_rights.append([int(float(now_video_annotation[4]) * self.width),
                                      int(float(now_video_annotation[5]) * self.height)])
                pass

            # 存储帧
            video_frames = []
            # 读取图片信息
            for now_frame in range(start_frame, end_frame):
                # read a frame
                ret, image = self.cap.read()
                if ret:
                    # 画框
                    if start_mask_frame < now_frame < end_mask_frame:
                        image = self._add_masks_in_image(image, left_tops, bottom_rights, action_ids)
                    video_frames.append(image)
                    # exit if Escape is hit
                    if cv2.waitKey(10) == 27:
                        is_break = True
                        break
                else:
                    raise Exception("执行中发生错误")
                pass

            # 保存视频
            self._images_to_video(video_frames, "{}/{}_{}_{}.mp4".format(self.result_path, i,
                                                                         int(middle_time), len(video_frames)))
            # 大视频 2
            for video_frame in video_frames:
                large_video.write(video_frame)

            # 打印信息
            if i % 1 == 0:
                print("{} {}/{}/{}".format(datetime.now(), i, int(middle_time), len(self.video_annotations)))
                pass
            # 跳出
            if is_break:
                break
            pass

        # 大视频 3
        large_video.release()

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
    def run(self, is_all_time=True):
        print("wideo width:{},height:{},number:{},speed:{}".format(self.width, self.height,
                                                                   self.total_frame, self.speed_frame))
        self._video_from_ava(is_all_time)
        pass

    pass


if __name__ == "__main__":
    ava = AVA(video_filename="data/zR725veL-DI.mp4", annotations_filename="data/ava_test_v1.0.csv",
              result_path="result/zR725veL-DI")
    ava.run(is_all_time=True)
