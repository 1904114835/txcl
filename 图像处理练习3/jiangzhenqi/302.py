import imageio
import matplotlib.pyplot as plt
import numpy as np

def convolve(I,F,iw,ih,fw,fh):
    """
    I:灰度图像，其分辨率是iw× ih
    F:一个滤波器，其大小是 fw× fh 
    """
    O = np.zeros((ih,iw,3)).astype(np.uint8)
    print(O.shape)
    for i in range(O.shape[0]):
        for j in range(O.shape[1]):
            s=0
            for ti in range(fh):
                for tj in range(fw):
                    s+=I[i+ti][j+tj]*F[ti][tj]
            O[i, j] = s 
    O = O.astype(np.uint8)
    return O

def show(im):
	plt.ion()
	plt.imshow(im)
	plt.show()
	plt.close()

def padding0(im):
    I = np.zeros((im.shape[0] + 2, im.shape[1] + 2,3)).astype(np.float32)
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            I[i + 1, j + 1] = im[i, j]
    I[0, :] = I[2, :]
    I[-1, :] = I[-3, :]
    I[:, 0] = I[:, 2]
    I[:, -1] = I[:, -3]
    I[0, 0] = I[0, 2]
    I[-1, 0] = I[-1, 2]
    I[0, -1] = I[0, -3]
    I[-1, -1] = I[-1, -3]
    return I

#主函数
file_in = '1.jpg'
file_out = '2.jpg'

#读入图像
im = imageio.imread(file_in)

#显示图像
plt.ion() 
plt.imshow(im)
plt.show()
plt.close()

F = np.array([[1/4,1/4],
              [1/4,1/4]])
ih = im.shape[0]
iw = im.shape[1]
fw = F.shape[0]
fh = F.shape[1]
print(im.shape)
I = padding0(im)
print(I.shape)
O = convolve(I,F,iw,ih,fw,fh)

show(O)
# 保存生成结果
#imageio.imwrite(file_out, O)

pause=1; 