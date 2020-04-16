import rotate_image
import cv2
import numpy as np
import imageio 
import matplotlib.pyplot as plt
def show(im):
    plt.ion() 
    plt.imshow(im)
    plt.show()
    
def rotate_bound(image, angle):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(image, M, (nW, nH))

path='C:/Users/19041/Desktop/im_Image Processing/crooked_horizon.jpg'
im=imageio.imread(path)
angle=45
myim=rotate_image.rotate_image(im,angle)
cvim=rotate_bound(im,-angle)

tim=np.zeros(cvim.shape).astype('uint8')
for i in range(len(myim)):
    for j in range(len(myim[0])):
        tim[i+1][j+1]=myim[i][j]
    
show(cvim-tim)