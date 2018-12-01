import cv2

# cap = cv2.VideoCapture("/home/ubuntu/data1.5TB/异常dataset/DAVIS/DAVIS-2017-TrainVal.mp4")

cap = cv2.VideoCapture(0)

cap.set(3, 1480)
cap.set(4, 1024)

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)

        if cv2.waitKey(30) & 0xff == "q":
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
