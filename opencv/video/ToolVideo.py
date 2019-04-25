import os
import cv2


def video_to_images(video_filename, is_save=True, result_path=None):

    if is_save:
        if result_path is None:
            result_path = os.path.splitext(video_filename)[0]
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        pass

    # capture the video
    vid_cap = cv2.VideoCapture(video_filename)
    total_frame = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 可能不准

    # start processing
    print("There are {} frames in the video {}".format(total_frame, video_filename))

    video_frame = []
    count = 0
    while True:
        ret, frame = vid_cap.read()
        if ret:
            if is_save:
                cv2.imwrite("{}/{}.jpg".format(result_path, count), frame)
            else:
                frame = cv2.resize(frame, dsize=(1080, 720))
                video_frame.append(frame)

            count += 1

            if cv2.waitKey(1) & 0xff == "q":
                break
        else:
            break

        # print the progress bar
        if count % 10 == 0:
            print("Done {}/{}".format(count, total_frame))

        pass

    cv2.destroyAllWindows()
    vid_cap.release()
    print("Done 100%")

    return video_frame, count


def images_to_video(video_folder, first_frame, last_frame, rep=5, images=None, result_filename=None):

    if result_filename is None:
        result_filename = "{}.avi".format(video_folder)

    if images is None:
        # read the first frame and find the height, width and layers of all the images
        img = cv2.imread(video_folder + '/{}.jpg'.format(first_frame))
        height, width, layers = img.shape
    else:
        height, width, layers = images[0].shape

    # initiate the video with width, height and pfs = 25
    # four_cc = cv2.VideoWriter_fourcc(*"XVID")  # avi
    four_cc = cv2.VideoWriter_fourcc(*"mp4v")  # mp4
    video = cv2.VideoWriter(result_filename, four_cc, 25, (width, height))

    total_frame = last_frame - first_frame + 1 if images is None else len(images)
    for i in range(total_frame):
        for j in range(rep):
            img = cv2.imread(video_folder + '/{}.jpg'.format(str(first_frame + i))) if images is None else images[i]
            video.write(img)

        # print the progress bar
        if i % 100 == 0:
            print("Done {}%".format((i*100)/(last_frame - first_frame)))

    cv2.destroyAllWindows()
    video.release()
    print("Done!")

    return None


def video_to_images_to_video(video_filename, result_filename):

    # capture the video
    vid_cap = cv2.VideoCapture(video_filename)
    total_frame = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 可能不准

    # start processing
    print("There are {} frames in the video {}".format(total_frame, video_filename))
    count = 1
    ret, frame = vid_cap.read()
    if ret:
        height, width, layers = frame.shape

        # initiate the video with width, height and pfs = 25
        four_cc = cv2.VideoWriter_fourcc(*"XVID")  # avi
        # four_cc = cv2.VideoWriter_fourcc(*"mp4v")  # mp4
        video = cv2.VideoWriter(result_filename, four_cc, 25, (width, height))
        video.write(frame)

        while True:
            ret, frame = vid_cap.read()
            if ret:
                video.write(frame)
                count += 1

                if cv2.waitKey(1) & 0xff == "q":
                    break
            else:
                break

            # print the progress bar
            if count % 10 == 0:
                print("Done {}/{}".format(count, total_frame))

            pass

    cv2.destroyAllWindows()
    vid_cap.release()
    print("Done 100%")

    return count


def crop_video(video_filename, result_filename, crop_area):

    # capture the video
    vid_cap = cv2.VideoCapture(video_filename)
    total_frame = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 可能不准

    # start processing
    print("There are {} frames in the video {}".format(total_frame, video_filename))
    count = 1
    ret, frame = vid_cap.read()
    if ret:
        height, width, layers = frame.shape
        crop_width = crop_area[2] - crop_area[0]
        crop_height = crop_area[3] - crop_area[1]
        if height < crop_height or width < crop_width or crop_area[0] < 0\
                or crop_area[2] < 0 or crop_area[1] >= width or crop_area[3] >= height:
            raise Exception("height < crop_height or width < crop_width")
            pass

        # initiate the video with width, height and pfs = 25
        four_cc = cv2.VideoWriter_fourcc(*"XVID")  # avi
        # four_cc = cv2.VideoWriter_fourcc(*"mp4v")  # mp4
        video = cv2.VideoWriter(result_filename, four_cc, 25, (crop_width, crop_height))
        video.write(frame)

        while True:
            ret, frame = vid_cap.read()
            if ret:

                frame = frame[crop_area[1]:crop_area[3], crop_area[0]:crop_area[2], :]
                video.write(frame)
                count += 1

                if cv2.waitKey(1) & 0xff == "q":
                    break
            else:
                break

            # print the progress bar
            if count % 10 == 0:
                print("Done {}/{}".format(count, total_frame))

            if count == 26 * 10:
                break

            pass

    cv2.destroyAllWindows()
    vid_cap.release()
    print("Done 100%")

    return count


if __name__ == "__main__":

    # video_to_images("test/test.mp4")
    # images_to_video("../plt/bear/bottom", 0, 7, 5)

    # image_path = "./eccv"
    # image_file = os.listdir(image_path)
    # for image_file_one in image_file:
    #     image_file_one_new = image_file_one.split("g")[1].split(".")[0]
    #     image_file_one_new = "" + str(int(image_file_one_new)) + ".jpg"
    #     os.rename(os.path.join(image_path, image_file_one), os.path.join(image_path, image_file_one_new))
    #     pass
    # video_to_images("/home/ubuntu/PycharmProjects/ALISURE/opticalflow/flownet2-pytorch/chen/chenlaoshi.avi", True,
    #                 result_path="/home/ubuntu/PycharmProjects/ALISURE/opticalflow/flownet2-pytorch/chen/image")
    images_to_video("/home/ubuntu/PycharmProjects/ALISURE/opticalflow/flownet2-pytorch/chen/run-video3", 0, 373, 1,
                    result_filename="/home/ubuntu/PycharmProjects/ALISURE/opticalflow/flownet2-pytorch/chen/chenlaoshi_3.mp4")
