"""
    打开手机的摄像头：网络摄像头
    手机上需要安装软件
"""
import cv2

cv2.namedWindow("Camera", 1)

# 开启IP摄像头
video = "http://admin:admin@172.24.54.11:8081"
cap = cv2.VideoCapture(video)

# 检查是否初始化成功，循环读取每一帧
while cap.isOpened():
    # 先返回一个布尔值，如果视频读取正确，则为 True，如果错误，则为 False，也可用来判断是否到视频末尾
    # 再返回一个值，为每一帧的图像，该值是一个三维矩阵
    ret, frame = cap.read()
    cv2.imshow("capture", frame)

    k = cv2.waitKey(1) & 0xFF  # 每帧数据延时1ms，延时不能为0，否则读取的结果会是静态帧
    if k == ord('s'):  # 若检测到按键's'，打印字符串
        print(cap.get(3))
        print(cap.get(4))
    elif k == ord("q"):  # 若检测到按键'q'，退出
        break

# 释放摄像头
cap.release()
# 删除创建的全部窗口
cv2.destroyAllWindows()