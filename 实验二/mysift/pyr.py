import numpy as np
import conv
import imageio
import imresize
import matplotlib.pyplot as plt
import cv2

def listImShow(im):
    plt.figure()
    for i in range(1,len(im)+1):
        plt.subplot(1,len(im),i)
        if len(np.shape(im[0]))==2:   
            plt.imshow(im[i-1].astype(np.int),cmap=plt.cm.gray)
        else:
            plt.imshow(im[i-1].astype(np.int))
        plt.xticks([])
        plt.yticks([])
    plt.show()
    plt.close()

def listImWrite(im,path,t='_'):
    for i in range(len(im)):
#        print(path+t+str(i)+'.jpg')
        imageio.imwrite(path+t+str(i)+'.jpg', im[i].astype(np.uint8))

def gskernel(size,sigma=1.0):
    gskernel=np.zeros((size,size),np.float64)
    for i in range (size):
        for j in range (size):
            norm=pow(i-1,2)+pow(j-1,2)
            gskernel[i,j]=np.exp(-norm/(2*pow(sigma,2)))
    s=np.sum(gskernel)
    kernel=gskernel/s
    return kernel

def gdown(im):
    for i in range(int(im.shape[0]/2)):
        for j in range(int(im.shape[1]/2)):
            im[i][j]=im[2*i][2*j]
    return im
    
#输入k层高斯，返回k+1层高斯
def gup(im):
    F=gskernel(3,1)
#    for i in F:
#        print(i)
    t=conv.Convolve(im,F)#高斯滤波
    t=gdown(t)#下采样
    return t[0:int(im.shape[0]/2),0:int(im.shape[1]/2)]

def getGpyr(im):
    gsim=[]
    gsim.append(im.astype(np.uint8))
    tim=im
    n=0
    while tim.shape[0]>3:
        tim=gup(tim)
        gsim.append(tim)
        n+=1
    return gsim

def lpyr(gsim):
    lplcim=[]
    for i in range(len(gsim)-1):
#        t=gsim[i]-imresize.imresize(gsim[i+1],gsim[i].shape)
        t=gsim[i]-conv.Convolve(imresize.imresize(gsim[i+1],gsim[i].shape),gskernel(3,1),3)
#        tmin=t.min()
#        t=t+abs(tmin)
#        tmax=t.max()
#        t=t/tmax*255.0
        lplcim.append(t)
    return lplcim
def yanzheng(g,l):
    huanyuan=[]
    for i in range(len(l)):
        t=l[i]+conv.Convolve(imresize.imresize(g[i+1],g[i].shape),gskernel(3,1),3)
        huanyuan.append(t)
    listImShow(huanyuan)
    return huanyuan
    
def beforeshow(list_im):
    for i in range(len(list_im)):
        tmin=list_im[i].min()
#        if tmin<0:
#            for j in range(len(im[i])):
#                for k in range(len(im[i][j])):
#                    for l in range(len(im[i][j][k])):
#                        if im[i][j][k][l]<0:
#                            im[i][j][k][l]=0
        list_im[i]=list_im[i]+abs(tmin)
        tmax=list_im[i].max()
        if tmax>255:
            list_im[i]=list_im[i]/tmax*255.0
    return list_im
if __name__=='__main__':
    path='C:/Users/19041/Desktop/图像处理/图像处理作业/实验一/'
    name='1.jpg'
    im = imageio.imread(path+name,as_gray=0).astype('float64')

    g=[]
    l=[]
    huanyuan=[]
    lshow=[]
    
    g=getGpyr(im)
    l=lpyr(g)
    
    listImWrite(g,path,'g')
    listImWrite(l,path,'l')
    huanyuan=yanzheng(g,l)    
    
    listImShow(g)
    listImShow(l)
    
    lshow=beforeshow(l)
    listImShow(lshow)
    
    listImWrite(l,path,'showl')
    listImWrite(huanyuan,path,'reBuild')
        