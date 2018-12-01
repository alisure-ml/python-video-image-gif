import os
import cv2

video_orig_path = "D:\\video"
video_deal_path = "D:\\video\\video_deal"

all_video_orig = [video_orig for video_orig in os.listdir(video_orig_path) if ".mp4" in video_orig]

for video_now_name in all_video_orig:
    video_now_path = os.path.join(video_orig_path, video_now_name)
    cap = cv2.VideoCapture(video_now_path)

    print(cap.get(3))
    print(cap.get(4))

    ret, frame = cap.read()
    if ret:
        save_image_path = os.path.join(video_deal_path,
                                       "{}.jpg".format(os.path.splitext(os.path.basename(video_now_name))[0]))
        cv2.imwrite(save_image_path, frame)
        pass

    cap.release()
    cv2.destroyAllWindows()
    pass
