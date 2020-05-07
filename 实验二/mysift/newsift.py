import numpy as np
#imresize用于替换cv2的pyrUP和pyrDown，
#不过imresize由python写成，运算速度较慢这里先由cv2代替
#import imresize
import conv
import pyr
import cv2
import newkp as kp
import copy

class my_sift():
    def make_list_sigmond(self):
        for i in range(self.ceng*self.s):
            self.list_sigmond.append(1.6*2**(i/self.s))
    def set_muti_gpyr(self):
        
        self.make_list_sigmond()
        self.muti.append([])
        self.muti[0].append(self.im)
        for i in range(self.ceng):
            if i!=0:
                self.muti.append([])
                self.muti[i].append(cv2.pyrDown(self.muti[i-1][-3]))
            for j in range(self.s):
                self.muti[i].append(conv.Convolve(self.muti[i][0],pyr.gskernel(15,self.list_sigmond[self.ceng*i+j])))
    def muti_gpyr_show(self):
        for i in range(len(self.muti)):
            pyr.listImShow(self.muti[i])

    def set_dog(self):
        for i in range(self.ceng):
            self.dog.append([])
            for j in range(self.s):
                self.dog[i].append(abs(self.muti[i][j+1]-self.muti[i][j]))
                
    def dog_show(self):
        a=copy.deepcopy(self.dog)
        for i in range(len(a)):
#            for j in range(len(a[i])):
#                amin, amax = a[i][j].min(),a[i][j].max() # 求最大最小值
#                a[i][j] = (a[i][j]-amin)/(amax-amin)*255
            pyr.listImShow(a[i])
            
    def get_kp_and_feature(self,image):
        self.im=image
        self.muti=[]
        self.dog=[]
        self.feature=[]
        self.kp=[]
        self.list_sigmond=[]
        self.s=5
        self.ceng=4
        #创建多层高斯金字塔
        self.set_muti_gpyr()
        #设置dog金字塔
        self.set_dog()
        #显示高斯金字塔
        self.muti_gpyr_show()
        #显示dog
        self.dog_show()
        
        #获得kp和feature
        self.kp,self.feature = kp.get_keypoints(self.dog,self.muti)
        
        print(np.shape(self.kp))
        print(np.shape(self.feature))
        return self.kp,self.feature
        
    def show_im_and_kp(self):
        tim=copy.deepcopy(self.im)
        for i in range(len(self.kp)):
            tim[self.kp[i][0]][self.kp[i][1]]=255
        conv.show(tim)
        
if __name__=='__main__':
    imageA = cv2.imread("1.jpg").astype(np.uint8)
    #imageA = cv2.imread("left_01.png")
    imageA = cv2.cvtColor(imageA,cv2.COLOR_BGR2GRAY)
    conv.show(imageA)  
    sift=my_sift()
    sift.get_kp_and_feature(imageA.astype(np.uint8))
    sift.show_im_and_kp()
    print(sift.feature[0])
    
    
    