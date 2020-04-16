import conv
import numpy as np
F=np.array(
            [
            [-1,-1,-1],
            [-1, 8,-1],
            [-1,-1,-1]
            ]
            )
F2=np.array(
            [
            [1/9,1/9,1/9],
            [1/9,1/9,1/9],
            [1/9,1/9,1/9]
            ]
            )
print(conv.getFmid(F2,10,10,9,9))
