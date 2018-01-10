import os
import cv2


def video_to_images(video_filename, result_path=None):

    if result_path is None:
        result_path = os.path.splitext(video_filename)[0]
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # capture the video
    vid_cap = cv2.VideoCapture(video_filename)
    total_frame = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # start processing
    print("There are {} frames in the video {}".format(total_frame, video_filename))

    video_frame = []
    for i in range(total_frame):

        # read a frame
        success, image = vid_cap.read()

        # save as a JPEG file
        cv2.imwrite("{}/{}.jpg".format(result_path, i), image)

        # exit if Escape is hit
        if cv2.waitKey(10) == 27:
            break

        # print the progress bar
        if i % 10 == 0:
            print("Done {}/{}".format(i, total_frame))

        pass

    cv2.destroyAllWindows()
    vid_cap.release()
    print("Done 100%")

    return video_frame


def images_to_video(video_folder, first_frame, last_frame, rep=5, result_filename=None):

    if result_filename is None:
        result_filename = "{}.avi".format(video_folder)

    # read the first frame and find the height, width and layers of all the images
    img = cv2.imread(video_folder + '/{}.jpg'.format(first_frame))
    height, width, layers = img.shape

    # initiate the video with width, height and pfs = 25
    video = cv2.VideoWriter(result_filename, -1, 25, (width, height))

    for i in range(last_frame - first_frame + 1):
        for j in range(rep):
            img = cv2.imread(video_folder + '/{}.jpg'.format(str(first_frame + i)))
            video.write(img)

        # print the progress bar
        if i % 100 == 0:
            print("Done {}%".format((i*100)/(last_frame - first_frame)))

    cv2.destroyAllWindows()
    video.release()
    print("Done!")

    return None


if __name__ == "__main__":

    video_to_images("test/test.mp4")
    # images_to_video("test/test", 0, 105, 1)
