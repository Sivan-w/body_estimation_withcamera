
import math
import time as ti


class PoseAnalyzer:

    words = "你好"

    def __init__(self,result):
        self.points = result['candidate'].astype('int32')
        self.index = result['subset'].astype('int32')

    def neck_infer_pose(self,point_0,point_1):
        print('由于信息不足，开始预测头部姿态.....')
        if (point_0[1].astype('float')-point_1[1])*(point_0[1]-point_1[1])/(point_0[0]-point_1[0])/(point_0[0]-point_1[0]) < 3 :
            return False
        else:
            return True

    def advice(self, word):
        self.words= self.words+"\n"+word

    def cal_ang(self,point_1, point_2, point_3):
        """
        根据三点坐标计算夹角
        :param point_1: 点1坐标
        :param point_2: 点2坐标
        :param point_3: 点3坐标
        :return: 返回任意角的夹角,这里规定point_2为顶点
        """
        a=math.sqrt((point_2[0]-point_3[0])*(point_2[0]-point_3[0])+(point_2[1]-point_3[1])*(point_2[1] - point_3[1]))
        b=math.sqrt((point_1[0]-point_3[0])*(point_1[0]-point_3[0])+(point_1[1]-point_3[1])*(point_1[1] - point_3[1]))
        c=math.sqrt((point_1[0]-point_2[0])*(point_1[0]-point_2[0])+(point_1[1]-point_2[1])*(point_1[1]-point_2[1]))
        # A=math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
        B=math.degrees(math.acos((b*b-a*a-c*c)/(-2*a*c)))
        # C=math.degrees(math.acos((c*c-a*a-b*b)/(-2*a*b)))
        if B > 180:
            B = 360-B

        return B

    def logic_realize(self,neck=120,waist=80,infer=True):
        '''
        :监测颈部和腰部姿态
        :默认颈部夹角大于120度,腰部夹角大于80度为合格姿态,此参数可供用户自定义
        :infer，当图片内容包含的信息不足以计算人体姿态时，是否推测人体姿态，默认开启

        返回值：
        第一部分(bool)： 颈部，腰部，左膝盖，右膝盖姿态，正确（True），错误（False）
        第二部分（time）：本次执行判断的对应的时间，用于生成日志

        '''
        p1 = self.index[0,1]
        p0 = self.index[0,0]
        p8 = self.index[0,8]
        p9 = self.index[0,9]
        p10 = self.index[0,10]
        p11 = self.index[0,11]
        p12 = self.index[0,12]
        p13 = self.index[0,13]

        # print(p8)
        # print(self.points[p8,:2],"________________________")

        waist_angle = 0
        neck_angle = 0
        left_knee_angle = 0
        right_knee_angle = 0

        re_neck = False
        re_waist = False
        re_left_knee = False
        re_right_knee = False

        if self.index.shape[0] == 1:    # 此处暂行只判断单人场景

            '''头部角度计算'''

            if p8 != -1 and p1 != -1 and p0 != -1:
                neck_angle = self.cal_ang(self.points[p8,:2],self.points[p1, :2], self.points[p0, :2])
            else:
                self.advice("该图检测颈部姿态的关键点信息不足")
                # print("该图检测颈部姿态的关键点信息不足")


            '''腰部角度计算'''
            # 若能够同时识别腰部两个关键点
            # 则以两点中心点作为point_2
            if p9 != -1 and p8 != -1 and p1 != -1 and p11 != -1 :
                waist_angle = self.cal_ang(self.points[p9,:2],self.points[p8,:2],self.points[p1,:2])/2  + \
                              self.cal_ang(self.points[p9,:2],self.points[p11,:2],self.points[p1,:2])/2
            elif p9 != -1 and p8 != -1 and p1 != -1 :
               waist_angle = self.cal_ang(self.points[p9,:2],self.points[p8,:2],self.points[p1,:2])
            elif p9 != -1 and p11 != -1 and p1 != -1:
                waist_angle = self.cal_ang(self.points[p9,:2],self.points[p11,:2],self.points[p1,:2])
            else:
                self.advice("该图检测腰部姿态的关键点信息不足")
                # print("该图检测腰部姿态的关键点信息不足")

            '''膝盖角度'''
            if p8 != -1 and p9 != -1 and p10 != -1 :
                # 左脚（也许）
                left_knee_angle = self.cal_ang(self.points[p8,:2],self.points[p9,:2],self.points[p10,:2])
            else:
                self.advice("该图检测左膝姿态的关键点信息不足")
                print("该图检测左膝姿态的关键点信息不足")
            if p11 != -1 and p12 != -1 and p13 != -1 :
                # 右脚
                right_knee_angle = self.cal_ang(self.points[p11,:2],self.points[p12,:2],self.points[p13,:2])
            else:
                self.advice("该图检测右膝姿态的关键点信息不足")
                print("该图检测右膝姿态的关键点信息不足")

        # elif  （多人）

        # print(neck_angle,"yes")
        print("颈部夹角 ",neck_angle)
        print("腰部夹角 ",waist_angle)
        print("左膝角度 {}, 右膝角度 {}".format(left_knee_angle,right_knee_angle))
        print("------------------------------------------------")


        # 逻辑判断 脖子
        if neck_angle <120 and neck_angle != 0:
            print('头抬高一点')
        # 信息不足开始推测    
        elif  neck_angle == 0 and infer == True :
            infer = self.neck_infer_pose(self.points[p0,:2],self.points[p1,:2])
            if infer==True:
                   pass
            else:
                self.advice("头抬高一点")
                print('头抬高一点')
        else:
            self.advice("头部姿态正确")
            print('头部姿态正确')
            re_neck = True

        # 腰部
        if waist_angle <80 and waist_angle != 0:
            self.advice("挺直腰背")
            print("挺直腰背")
        else:
            self.advice("腰部姿态正确")
            print('腰部姿态正确')
            re_waist = True

        # 膝盖
        if left_knee_angle < 100 and left_knee_angle >70 :
            self.advice("左膝姿态错误")
            print('左膝姿态错误')
        else:
            re_left_knee = True
        if  right_knee_angle < 100 and right_knee_angle >70 :
            self.advice("右膝姿态错误")
            print('右膝姿态错误')
        else:
            re_right_knee = True
        if re_right_knee == True and re_left_knee == True:
            self.advice("膝盖姿态正确")
            print('膝盖姿态正确')

        time = ti.strftime("%Y-%m-%d %H:%M:%S", ti.localtime())

        return self.words
        # return   re_neck,re_waist,re_left_knee,re_right_knee,time
