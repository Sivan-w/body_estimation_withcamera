import cv2


def from_cra(cra=0, time=5000 - 300, show=0):
    '''
    cra 为摄像头设置
    0：内置摄像头
    1：外接摄像头

    time 为获取图片的间隔时间（ms）

    show 是否展示获取到的图片
    1:Yes

    '''

    cap = cv2.VideoCapture(0)  # 打开默认摄像头采集图像

    width = 640  # 定义摄像头获取图像宽度
    height = 480  # 定义摄像头获取图像长度

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # 设置宽度
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # 设置长度

    # cap.set(4,600)
    ret, frame = cap.read(cv2.IMREAD_ANYCOLOR)
    # ret = False
    if ret == False:
        raise Exception("Exception:Fail to take photo")
        # img=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) ##BGR图转RGB图
    img = frame
    if show == 1:
        cv2.imshow("capture", img)

    k = cv2.waitKey(time)
    cap.release()
    cv2.destroyAllWindows()
    return img
