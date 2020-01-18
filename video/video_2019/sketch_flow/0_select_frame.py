import os
import cv2
from alisuretool.Tools import Tools


def select_frame(video_filename, begin_frame=0, end_frame=None, result_file_name=None, is_second=False, is_save_image=False):
    # capture the video
    vid_cap = cv2.VideoCapture(video_filename)
    total_frame = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 可能不准
    frame_fps = int(vid_cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if is_second:
        begin_frame = begin_frame * frame_fps
        end_frame = end_frame * frame_fps
        pass

    if begin_frame < total_frame:
        vid_cap.set(cv2.CAP_PROP_POS_FRAMES, begin_frame)
        pass

    # start processing
    Tools.print("There are {} frames in the video {}".format(total_frame, video_filename))

    four_cc = cv2.VideoWriter_fourcc(*"XVID")  # avi
    result_video = cv2.VideoWriter(result_file_name, four_cc, 25, (frame_width, frame_height))

    count = 0
    video_frame = []
    while True:
        ret, frame = vid_cap.read()
        if ret:
            if is_save_image:
                result_path = Tools.new_dir(os.path.splitext(result_file_name)[0])
                cv2.imwrite("{}/{}.jpg".format(result_path, count), frame)
                pass
            result_video.write(frame)
            count += 1
            if cv2.waitKey(1) & 0xff == "q":
                break
        else:
            break

        if count + begin_frame >= end_frame:
            break

        # print the progress bar
        if count % 10 == 0:
            Tools.print("Done {}/{}".format(count, total_frame))
            pass

        pass

    cv2.destroyAllWindows()
    vid_cap.release()
    Tools.print("Done 100%")

    return video_frame, count


if __name__ == '__main__':
    # _input_path = "/home/ubuntu/data1.5TB/video/video_deal/show"
    # _result_path = Tools.new_dir("/home/ubuntu/data1.5TB/video/video_deal/select_video/video")
    # _video_filename = "20180707_20180707091950_20180707092036_092247.avi"

    # _input_path = "/home/ubuntu/data1.5TB/video/video_deal/long"
    # _video_filename = "20180523_20180523155357_20180523174805_155633.mp4"
    # _begin_frame, _end_frame = 29 * 60 + 0, 29 * 60 + 8
    # _begin_frame, _end_frame = 38 * 60 + 15, 38 * 60 + 20
    # _begin_frame, _end_frame = 63 * 60 + 37, 63 * 60 + 55

    # _input_path = "/home/ubuntu/data1.5TB/video/video_deal/long"
    # _video_filename = "20180707_20180707092133_20180707093648_092428.mp4"
    # _begin_frame, _end_frame = 0 * 60 + 0, 0 * 60 + 4

    # _input_path = "/home/ubuntu/data1.5TB/异常dataset/ShanghaiTech/test/test_video"
    # _video_filename = "01_0053电动三轮车.avi"
    # _begin_frame, _end_frame = 0 * 60 + 5, 0 * 60 + 8
    # _video_filename = "10_0074摩托车.avi"
    # _begin_frame, _end_frame = 0 * 60 + 20, 0 * 60 + 23
    # _video_filename = "05_0019聚众推搡.avi"
    # _begin_frame, _end_frame = 0 * 60 + 7, 0 * 60 + 13

    _input_path = "/home/ubuntu/data1.5TB/异常dataset/ShanghaiTech/train"
    # _video_filename = "05_043.avi"
    # _begin_frame, _end_frame = 0 * 60 + 15, 0 * 60 + 23
    _video_filename = "08_020.avi"
    _begin_frame, _end_frame = 0 * 60 + 5, 0 * 60 + 20

    _result_root = "/home/ubuntu/data1.5TB/video/video_deal/sketch_flow_2/select_video"
    _result_file_name = Tools.new_dir(os.path.join(
        _result_root, "{}_{}_{}.avi".format(os.path.splitext(_video_filename)[0], _begin_frame, _end_frame)))

    select_frame(os.path.join(_input_path, _video_filename), begin_frame=_begin_frame,
                 end_frame=_end_frame, result_file_name=_result_file_name, is_second=True)
    pass
