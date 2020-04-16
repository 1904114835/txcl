path='C:/Users/19041/Desktop/im_Image Processing/crooked_horizon.jpg'

import cv2
import numpy as np
import rotate_image

def get_angle():
    global angle,count_c
    c=count_c
    x1=ix[(c-2)%2]
    x2=ix[(c-1)%2]
    y1=iy[(c-2)%2]
    y2=iy[(c-1)%2]
    t_angle=np.arctan((y2-y1)/(x2-x1))#算出来是顺时针，进到函数里逆时针
    print("第一个点",x1,y1)
    print("第二个点",x2,y2)
    print("本次角度",t_angle/np.pi*180)
    angle+=t_angle#储存历史角度
    print("历史角度",angle/np.pi*180)
    return angle
    
def rot(event,x,y,flags,param):
    global count_c
    if event == cv2.EVENT_LBUTTONDOWN:
        ix[count_c%2]=x
        iy[count_c%2]=y
        count_c+=1
        if count_c%2==1:            
            cv2.imshow("Press Esc to exit",rotate_image.rotate_image(img,get_angle()/np.pi*180))
            

img = cv2.imread(path, 1)
ix=[-1 for i in range(2)]
iy=[-1 for i in range(2)]
count_c=1
angle=0

cv2.namedWindow('Press Esc to exit')
cv2.imshow("Press Esc to exit", img)

cv2.setMouseCallback('Press Esc to exit',rot)


while(1):
    if cv2.waitKey(100)==27:
        break
cv2.destroyAllWindows()
