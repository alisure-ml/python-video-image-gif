import numpy as np
import cv2


def optical_flow_from_video():
    cap = cv2.VideoCapture('test.mp4')

    # 设置 ShiTomasi 角点检测的参数
    feature_params = dict(maxCorners=100, qualityLevel=0.3,
                          minDistance=7, blockSize=7)
    # 设置 lucas kanade 光流场的参数
    # maxLevel 为使用图像金字塔的层数
    lk_params = dict(winSize=(15, 15), maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    # 产生随机的颜色值
    color = np.random.randint(0, 255, (100, 3))

    # 获取第一帧，并寻找其中的角点
    _, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

    # 创建一个掩膜为了后面绘制角点的光流轨迹
    mask = np.zeros_like(old_frame)

    while True:
        ret, frame = cap.read()
        if ret:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 计算能够获取的角点的新位置
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
            # Select good points
            good_new = p1[st == 1]
            good_old = p0[st == 1]
            # 绘制角点的轨迹
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
                frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)

            img = cv2.add(frame, mask)

            cv2.imshow('frame', img)
            if cv2.waitKey(30) & 0xff == ord("q"):
                break

            # 更新当前帧和当前角点的位置
            old_gray = frame_gray.copy()
            p0 = good_new.reshape(-1, 1, 2)
        else:
            break

        pass

    cv2.destroyAllWindows()
    cap.release()

    pass


def optical_flow_from_camera():
    cap = cv2.VideoCapture(0)

    # 设置 ShiTomasi 角点检测的参数
    feature_params = dict(maxCorners=100, qualityLevel=0.3,
                          minDistance=7, blockSize=7)
    # 设置 lucas kanade 光流场的参数
    # maxLevel 为使用图像金字塔的层数
    lk_params = dict(winSize=(15, 15), maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    # 产生随机的颜色值
    color = np.random.randint(0, 255, (100, 3))

    # 获取第一帧，并寻找其中的角点
    _, old_frame = cap.read()
    old_frame = cv2.flip(old_frame, 1)
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

    # 创建一个掩膜为了后面绘制角点的光流轨迹
    mask = np.zeros_like(old_frame)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 计算能够获取的角点的新位置
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
            # Select good points
            good_new = p1[st == 1]
            good_old = p0[st == 1]
            # 绘制角点的轨迹
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
                frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)

            img = cv2.add(frame, mask)

            cv2.imshow('frame', img)
            if cv2.waitKey(30) & 0xff == ord("q"):
                break

            # 更新当前帧和当前角点的位置
            old_gray = frame_gray.copy()
            p0 = good_new.reshape(-1, 1, 2)
        else:
            break

        pass

    cv2.destroyAllWindows()
    cap.release()

    pass


def optical_flow_from_camera_farneback2():
    cap = cv2.VideoCapture(0)

    cap.set(3, 640)
    cap.set(4, 480)

    ret, frame1 = cap.read()
    frame1 = cv2.flip(frame1, 1)
    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    while True:
        try:
            ret, frame2 = cap.read()
            frame2 = cv2.flip(frame2, 1)
        except Exception:
            break
            pass

        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 1)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        result = np.concatenate((frame2, rgb), axis=1)
        cv2.imshow('result', result)

        if cv2.waitKey(1) & 0xff == "q":
            break
        prvs = next
        pass

    cap.release()
    cv2.destroyAllWindows()

    pass


def optical_flow_from_camera_farneback(flip=True, resize=True):
    # cap = cv2.VideoCapture('test.mp4')
    cap = cv2.VideoCapture('test2.ts')
    # cap = cv2.VideoCapture('eccv.avi')
    # cap = cv2.VideoCapture(0)

    width = 640
    height = 480
    cap.set(3, width)
    cap.set(4, height)

    ret, frame1 = cap.read()
    if flip:
        frame1 = cv2.flip(frame1, 1)
    if resize:
        frame1 = cv2.resize(frame1, (width, height), interpolation=cv2.INTER_CUBIC)
    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    while True:
        try:
            ret, frame2 = cap.read()
            if flip:
                frame2 = cv2.flip(frame2, 1)
            if resize:
                frame2 = cv2.resize(frame2, (width, height), interpolation=cv2.INTER_CUBIC)
            cv2.imshow('frame1', frame2)
        except Exception:
            break
            pass

        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 20, 3, 5, 1.2, 1)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        cv2.imshow('frame2', rgb)

        result = np.concatenate((frame2, rgb), axis=1)
        cv2.imshow('result', result)

        if cv2.waitKey(1) & 0xff == "q":
            break
        prvs = next
        pass

    cap.release()
    cv2.destroyAllWindows()

    pass


def optical_flow_from_camera_farneback_and_write_video():
    cap = cv2.VideoCapture('eccv.avi')

    width = 640
    height = 480
    cap.set(3, width)
    cap.set(4, height)

    ret, frame1 = cap.read()
    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255

    i = 0

    while True:
        try:
            ret, frame2 = cap.read()

            next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 20, 3, 5, 1.2, 1)
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            hsv[..., 0] = ang * 180 / np.pi / 2
            hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
            rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

            result = np.concatenate((frame2, rgb), axis=1)
            cv2.imshow('result', result)

            i += 1
            cv2.imwrite("{}/{}.jpg".format("eccv", str(i)), result)

            if cv2.waitKey(1) & 0xff == "q":
                break
            prvs = next
        except Exception:
            break
        pass

    cap.release()
    cv2.destroyAllWindows()
    pass


if __name__ == '__main__':
    optical_flow_from_camera_farneback2()
    pass
