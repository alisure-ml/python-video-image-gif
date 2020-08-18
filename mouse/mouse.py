import cv2
import os
import numpy as np
from alisuretool.Tools import Tools

result_dir = "D:/mouse"
result_name = "08-14-2"
cap = cv2.VideoCapture(1)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
background_sub_tractor_mog2 = cv2.createBackgroundSubtractorMOG2()

count = 0
while True:
    ret, frame = cap.read()
    if ret:
        mask = background_sub_tractor_mog2.apply(frame)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        if np.sum(mask // 125) > 1000:
            count += 1
            Tools.print("{} {}".format(Tools.get_format_time(), count))
            if count > 5:
                file_name = "{}_{}.png".format(Tools.get_format_time().replace(":", "_"), count)
                result_file_name = os.path.join(result_dir, result_name, file_name)
                cv2.imwrite(Tools.new_dir(result_file_name), frame)
            pass

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)

        if cv2.waitKey(30) & 0xff == "q":
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
