# 内部模块的调试

import paddlehub as hub
from pandas import array
import caculate_angle as ca
import numpy as np
from get_images import from_cra as cra

img = cra(1)
model = hub.Module(name='openpose_body_estimation')
result = model.predict(img, visualization=True)
p = ca.PoseAnalyzer(result)
res = p.logic_realize()
print(res)
