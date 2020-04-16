import numba
import numpy as np
import time
@numba.jit
def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result

a=np.random.rand(1000,1000)

s=time.time()
print(sum2d(a))
e=time.time()
print(e-s)