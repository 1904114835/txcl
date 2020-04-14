import numpy as np
import matplotlib.pyplot as plt

def show(im):
    #通过判断形状控制是否灰度显示
    if len(im.shape) == 2:
        plt.ion() 
        plt.imshow(im,cmap='gray')
        plt.show()
        plt.close()
    else:
        plt.ion() 
        plt.imshow(im)
        plt.show()
        plt.close()
    return 0
def getFmid(F,h,w,i,j):
    tF=np.zeros(F.shape).astype('float')
    fh=F.shape[0]
    fw=F.shape[1]
    bh=int((fh-1)/2)
    bw=int((fw-1)/2)
    #对行进行重新加权
    if i-bh<0:
        up=abs(i-bh)
#        print(up)
        for tj in range(fw):
            tsall=F[:,tj].sum()
            tstemp=F[up:fh,tj].sum()
            #计算
#            print('局部和',tsall,tstemp)
            for ti in range(fw):
                if ti>=up:
                    if tstemp!=0:
                        tF[ti][tj]=tsall/tstemp*F[ti][tj]
                    else:
                        tF[ti][tj]=0
                else:
                    tF[ti][tj]=0
        F=tF  
    if i+bh>h-1:
        down=fh-(i+bh-h+1)-1
        #print(down)
        for tj in range(fw):
            tsall=F[:,tj].sum()
            tstemp=F[0:down+1,tj].sum()
            #计算
#            print('局部和',tsall,tstemp)
            for ti in range(fw):
                if ti<=down:
                    if tstemp!=0:
                        tF[ti][tj]=tsall/tstemp*F[ti][tj]
                    else:
                        tF[ti][tj]=0
                else:
                    tF[ti][tj]=0
        F=tF  
    if j-bw<0:
#        print(tF)
        l=abs(j-bw)
        for ti in range(fh):
            tsall=sum(F[ti])
            tstemp=F[ti][l:fw].sum()
            #计算
            for tj in range(fw):
                if tj>=l:
                    if tstemp!=0:
                        tF[ti][tj]=tsall/tstemp*F[ti][tj]
                    else:
                        tF[ti][tj]=0
                else:
                    tF[ti][tj]=0
                    
    #列加权
        F=tF
    if j+bw>w-1:
        r=fw-(j+bw-w+1)-1
#        print(r)
        for ti in range(fh):
            tsall=sum(F[ti])
            tstemp=F[ti,0:r+1].sum()
            #计算
            for tj in range(fw):
                if tj<=r:
                    if tstemp!=0:
                        tF[ti][tj]=tsall/tstemp*F[ti][tj]
                    else:
                        tF[ti][tj]=0
                else:
                    tF[ti][tj]=0
    #列加权
        F=tF

    return tF
#由于只在边界生效，所以当输入不在边界时认为产生错误调用返回全空
def getF(F,h,w,i,j):
    tF=np.zeros(F.shape).astype('float')
    fh=F.shape[0]
    fw=F.shape[1]
    #对行进行重新加权
    if j-fw<-1:
        l=fw-j-1
        for ti in range(fh):
            tsall=sum(F[ti])
            tstemp=0.0
            for tstj in range(l,fw):
                tstemp+=F[ti][tstj]
            #计算
            for tj in range(l,fw):
                tF[ti][tj]=tsall/tstemp*F[ti][tj]
    #列加权
        F=tF
    #print(F)
    if i+fh>h:
        down=fh-(i+fh-h)
        #print(down)
        for tj in range(fw):
            tsall=0.0
            tstemp=0.0
            for tsti in range(fh):
                tsall+=F[tsti][tj]
            for tsti in range(down):
                tstemp+=F[tsti][tj]
            #计算
            #print('局部和',tsall,tstemp)
            for ti in range(fw):
                if ti<down and tj+j-(fw-1)>=0:
                    tF[ti][tj]=tsall/tstemp*F[ti][tj]
                else:
                    tF[ti][tj]=0
    return tF

def Convolve(I, F,way=2,iw=0, ih=0, fw=0, fh=0):
    iw=I.shape[1]
    ih=I.shape[0]
    fw=F.shape[1]
    fh=F.shape[0]
    O=np.zeros(I.shape).astype(np.float64)
    bh=int((fh-1)/2)
    bw=int((fw-1)/2)
    tshape=list(I.shape)
    tshape[0]=ih+fh-1
    tshape[1]=iw+fw-1
    Y = np.zeros(tshape).astype(np.float64)
    Y[bh:ih+bh,bw:iw+bw]=I
    #第二种
    if way==2:
        Y[0:bh,0:-1]=Y[bh:2*bh,0:-1]
        Y[0:-1,0:bh]=Y[0:-1,bh:2*bh]
        Y[ih+bh:-1,0:-1]=Y[ih-bh:ih,0:-1]
        Y[0:-1,iw+bw:-1]=Y[0:-1,iw-bw:iw]
        if len(tshape)==3:
            s=np.zeros((3))
            for ti in range(int(O.shape[0]/2)):
                for tj in range(int(O.shape[1]/2)):
                    i=2*ti
                    j=2*tj
                    s[0]=(Y[i:i+fh,j:j+fw,0]*F).sum()
                    s[1]=(Y[i:i+fh,j:j+fw,1]*F).sum()
                    s[2]=(Y[i:i+fh,j:j+fw,2]*F).sum()
                    O[i][j] = s 
        else:
            for i in range(O.shape[0]):
                for j in range(O.shape[1]):
                    O[i][j]=(Y[i:i+fh,j:j+fw]*F).sum()
    #O=O.clip(0,255)
    return O.astype(np.float64)#在调用时使用float64

