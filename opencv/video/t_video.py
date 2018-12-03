import os
import cv2
import numpy as np
from ToolVideo import video_to_images
from PIL import Image, ImageDraw, ImageFont


def draw_one_data(image_file, txt="无人机航拍西电天桥", txt_xy=(80, 22), txt_color=(0, 0, 255)):
    im = Image.open(image_file).convert("RGB")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("simhei.ttf", 45, encoding="utf-8")
    draw.text(txt_xy, txt, txt_color, font=font)
    # im.show()
    return np.asarray(im)


def draw_one_data_bg(image_file, txt_1="ECO", txt_2="改进ECO",
                     bg_1_xy=(840, 22, 1030, 70), txt_1_xy=(910, 30),
                     bg_2_xy=(840, 430, 1030, 482), txt_2_xy=(880, 437),
                     txt_color=(0, 0, 0)):
    im = Image.open(image_file).convert("RGB")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("simhei.ttf", 35, encoding="utf-8")
    draw.rectangle(bg_1_xy, fill=(255, 255, 255))
    draw.text(txt_1_xy, txt_1, txt_color, font=font)
    draw.rectangle(bg_2_xy, fill=(255, 255, 255))
    draw.text(txt_2_xy, txt_2, txt_color, font=font)
    # im.show()
    return np.asarray(im)


def images_to_video(video_folder, first_frame, last_frame, rep=5, result_filename=None, draw_data=draw_one_data):

    if result_filename is None:
        result_filename = "{}.avi".format(video_folder)

    # read the first frame and find the height, width and layers of all the images
    img = cv2.imread(video_folder + '/{}.jpg'.format(first_frame))
    height, width, layers = img.shape

    # initiate the video with width, height and pfs = 25
    four_cc = cv2.VideoWriter_fourcc(*"XVID")  # avi
    # four_cc = cv2.VideoWriter_fourcc(*"mp4v")  # mp4
    video = cv2.VideoWriter(result_filename, four_cc, 25, (width, height))

    for i in range(last_frame - first_frame + 1):
        for j in range(rep):
            img = draw_data(video_folder + '/{}.jpg'.format(str(first_frame + i)))
            video.write(img)

        # print the progress bar
        if i % 100 == 0:
            print("Done {}%".format((i*100)/(last_frame - first_frame)))

    cv2.destroyAllWindows()
    video.release()
    print("Done!")

    return None


# media1.avi
# video_to_images(video_filename="../video2gif/video/media1.avi", result_path="./media1")
# bg_1_xy=(840, 22, 1030, 70), txt_1_xy=(910, 30),
# bg_2_xy=(840, 430, 1030, 482), txt_2_xy=(887, 430),
# images_to_video("./media1", 0, 300, 1, result_filename="./media/media1.avi", draw_data=draw_one_data_bg)

# media2.avi
# video_to_images(video_filename="../video2gif/video/media2.avi", result_path="./media2")
# bg_1_xy = (1120, 22, 1310, 70), txt_1_xy = (1190, 30),
# bg_2_xy = (1120, 800, 1310, 848), txt_2_xy = (1157, 810),
# images_to_video("./media2", 0, 300, 1, result_filename="./media/media2.avi", draw_data=draw_one_data_bg)

# media3.avi
# video_to_images(video_filename="../video2gif/video/media3.avi", result_path="./media3")
# bg_1_xy=(840, 22, 1030, 70), txt_1_xy=(910, 30),
# bg_2_xy=(840, 430, 1030, 482), txt_2_xy=(887, 430),
images_to_video("./media3", 0, 262, 1, result_filename="./media/media3.avi", draw_data=draw_one_data_bg)

# media4.avi
# video_to_images(video_filename="../video2gif/video/media4.avi", result_path="./media4")
# bg_1_xy=(1139, 22, 1329, 70), txt_1_xy=(1209, 30),
# bg_2_xy=(1139, 576, 1329, 624), txt_2_xy=(1176, 586),
# images_to_video("./media4", 0, 980, 1, result_filename="./media/media4.avi", draw_data=draw_one_data_bg)

# media5.avi
# video_to_images(video_filename="../video2gif/video/media7.avi", result_path="./media7")
# txt_xy = (1320, 22)

# images_to_video("./media7", 0, 299, 1, result_filename="./media/media7_l.avi", draw_data=draw_one_data)

# draw_one_data_bg("./media3/0.jpg")
