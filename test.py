# import tkinter
#
# top = tkinter.Tk()
# top.mainloop()

from show_infor import ui_show
import cv2
import paddlehub as hub

cap = cv2.VideoCapture(0)
model = hub.Module(name='openpose_body_estimation')
i = 0
while(1):
    ui_show(cap,model)
    i = i+1
    # if i==5:
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     break
