# 内部模块的调试

import paddlehub as hub
from pandas import array
import caculate_angle as ca
from show_infor import ui_show
import cv2
import pyttsx3
import tkinter as tk


class Application(tk.Frame):
    word = "你好"

    def listen(self, words):
        self.word = words

    def __init__(self,root):
        super().__init__(root)
        self.master = root
        self.pack()
        self.words()

    def words(self):
        tk.Label(self, text=self.word, fg='red',width=5,height=5).pack()


# root = tk.Tk()
# root.title('检测中...')
# applicate = Application(root=root)
# applicate.listen("jjjjjjj")
# root.mainloop()

cap = cv2.VideoCapture(0)

model = hub.Module(name='openpose_body_estimation')




while 1:
    res = ui_show(cap, model)
    blank = ""
    if res != blank:
        pass
        # applicate.listen(res)
        # root.mainloop()
    pyttsx3.speak(res)
    #     cap.release()
    #     cv2.destroyAllWindows()


    print(111)








