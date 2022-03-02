import cv2
import caculate_angle as ca

def ui_show(cap,model):
    
    res = []
    # cap = cv2.VideoCapture(0) #打开默认摄像头采集图像

    width = 640  #定义摄像头获取图像宽度
    height = 480   #定义摄像头获取图像长度

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)  #设置宽度
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  #设置长度

   
        # print('img type:',type(img))

        # while 1:
        # cap.set(4,600)
    ret, frame = cap.read(cv2.IMREAD_ANYCOLOR)
            # ret = False
    if ret == False:
         raise Exception("Exception:Fail to take photo")
         print('failllll')
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) ##BGR图转RGB图
    # cv2.imshow("capture", img)
    result = model.predict(frame, visualization=False)
    print('1')
    p = ca.PoseAnalyzer(result)
    print('2')
    res = p.logic_realize()
    print('3')
    img = result['data']
    cv2.imshow('img', img)
    k = cv2.waitKey(1)
    return res

