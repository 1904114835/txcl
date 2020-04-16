import numpy as np
import conv
import imageio
import imresize
import matplotlib.pyplot as plt

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

def listImWrite(im,path,t='none'):
    for i in range(len(im)):
#        print(path+t+str(i)+'.jpg')
        imageio.imwrite(path+t+str(i)+'.jpg', im[i].astype(np.uint8))

def gskernel(size,sigma):
    sigma=1.0
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
def Gsup(im):
    F=gskernel(3,1)
    t=conv.Convolve(im,F)#高斯滤波
    t=gdown(t)#下采样
    return t[0:int(im.shape[0]/2),0:int(im.shape[1]/2)]

def getpyr(im):
    gsim=[]
    gsim.append(im.astype(np.uint8))
    tim=im
    lplcim=[]
    n=0
    while tim.shape[0]>1:
        tim=Gsup(tim)
        gsim.append(tim)
        n+=1
    for i in range(n):
        t=gsim[i]-imresize.imresize(gsim[i+1],gsim[i].shape)
#        tmin=t.min()
#        t=t+abs(tmin)
#        tmax=t.max()
#        t=t/tmax*255.0
        lplcim.append(t)
    return gsim,lplcim
def yanzheng(g,l):
    huanyuan=[]
    for i in range(len(l)):
        t=(g[i]+l[i])
        huanyuan.append(t)
    listImShow(huanyuan)
    
def beforeshow(im):
    for i in range(len(im)):
        tmin=im[i].min()
        if tmin<0:
            im[i]=im[i]+abs(tmin)
        tmax=im[i].max()
        if tmax>255:
            im[i]=im[i]/tmax*255.0
    return im
if __name__=='__main__':
    path='C:/Users/19041/Desktop/图像处理/图像处理作业/实验一/'
    name='1.jpg'
    im = imageio.imread(path+name,as_gray=0).astype('float64')
    g=[]
    l=[]
    g,l=getpyr(im)

    listImWrite(g,path,'g')
    listImWrite(l,path,'l')
    yanzheng(g,l)    
    
    listImShow(g)
    tl=beforeshow(l)
    listImShow(l)
#    for i in g:
#        conv.show(i)
#    for i in l:
#        conv.show(i)
        