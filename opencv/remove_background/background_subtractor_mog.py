import cv2

cap = cv2.VideoCapture(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
background_sub_tractor_mog2 = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    if ret:
        mask = background_sub_tractor_mog2.apply(frame)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        cv2.imshow('frame', mask)

        if cv2.waitKey(30) & 0xff == "q":
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
