import numpy as np
import matplotlib.pyplot as plt
import imageio

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
    tF=np.zeros(F.shape).astype('float64')
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
    t=np.zeros(I[0][0].shape)
    if F.shape[0]%2==0:
    #    print(I.shape,F.shape,way)
        #第一种
        if way==1:
            for i in range(ih):
                for j in range(iw):
                    t=0
                    for fi in range(fw):
                        for fj in range(fh):
                            if i+fi<ih and i+fi>-1 and \
                            j-fw+1+fj<iw and j-fw+1+fj>-1:
                                t+=I[i+fi][j-fw+1+fj]*F[fi][fj]
                            else:
                                t+=0
                    O[i][j]=t
                    
        #第二种
        if way==2:
            for i in range(ih):
                for j in range(iw):
                    t=0
                    for fi in range(fh):
                        for fj in range(fw):
                            #若行爆
                            if i+fi>=ih:
                                ti=(ih-1)-abs(ih-1-i-fi)
                            else:
                                ti=i+fi
                            #若列爆
                            if j-fw+1+fj<0:
                                tj=abs(j-fw+1+fj)
                            else:
                                tj=j-fw+1+fj
                            t+=I[ti][tj]*F[fi][fj]
                    O[i][j]=t
        #第三种
        if way==3:
            for i in range(ih):
                for j in range(iw):
                    t=0
                    #若在边界
                    if i+fh-1>ih-1 or j-(fw-1)<0:
                        tF=getF(F,ih,iw,i,j,)
                        for fi in range(fh):
                            for fj in range(fw):
                                if i+fi<ih and j-fw+1+fj>-1:
                                    t+=I[i+fi][j-fw+1+fj]*tF[fi][fj]
                    else:
                        for fi in range(fh):
                            for fj in range(fw):
                                t+=I[i+fi][j-fw+1+fj]*F[fi][fj]
                    O[i][j]=t
    else:
        #中心对齐
        bh=int((fh-1)/2)
        bw=int((fw-1)/2)
        tshape=list(I.shape)
        tshape[0]=ih+fh-1
        tshape[1]=iw+fw-1
        Y = np.zeros(tshape).astype(np.float64)
        Y[bh:ih+bh,bw:iw+bw]=I
        
        if way==1:
            if len(tshape)==3:
                s=np.zeros((3))
                for i in range(O.shape[0]):
                    for j in range(O.shape[1]):
                        s[0]=(Y[i:i+fh,j:j+fw,0]*F).sum()
                        s[1]=(Y[i:i+fh,j:j+fw,1]*F).sum()
                        s[2]=(Y[i:i+fh,j:j+fw,2]*F).sum()
                        O[i][j] = s
            else:
                for i in range(O.shape[0]):
                    for j in range(O.shape[1]):
                        O[i][j]=(Y[i:i+fh,j:j+fw]*F).sum()
        #第二种
        if way==2:
            for i in range(bh):
                Y[i,0:-1]=Y[2*bh-1-i,0:-1]
                Y[ih+i,0:-1]=Y[ih-1-i,0:-1]
            for i in range(bw):
                Y[0:-1,i]=Y[0:-1,2*bh-1-i]
                Y[0:-1,iw+i]=Y[0:-1,iw-1-i]
            if len(tshape)==3:
                s=np.zeros((3))
                for i in range(O.shape[0]):
                    for j in range(O.shape[1]):
                        s[0]=(Y[i:i+fh,j:j+fw,0]*F).sum()
                        s[1]=(Y[i:i+fh,j:j+fw,1]*F).sum()
                        s[2]=(Y[i:i+fh,j:j+fw,2]*F).sum()
                        O[i][j] = s 
            else:
                for i in range(O.shape[0]):
                    for j in range(O.shape[1]):
                        O[i][j]=(Y[i:i+fh,j:j+fw]*F).sum()
        #第三种
        if way==3:
            if len(tshape)==3:
                s=np.zeros((3))
                for i in range(ih):
                    for j in range(iw):
                        #若在边界
                        if i-bh<0 or i+bh>ih-1 or j-bw<0 or j+bw>iw-1 :
                            tF=getFmid(F,ih,iw,i,j,)
                            s[0]=(Y[i:i+fh,j:j+fw,0]*tF).sum()
                            s[1]=(Y[i:i+fh,j:j+fw,1]*tF).sum()
                            s[2]=(Y[i:i+fh,j:j+fw,2]*tF).sum()
                        else:
                            s[0]=(Y[i:i+fh,j:j+fw,0]*F).sum()
                            s[1]=(Y[i:i+fh,j:j+fw,1]*F).sum()
                            s[2]=(Y[i:i+fh,j:j+fw,2]*F).sum()
                        O[i][j] = s
            else:
                for i in range(ih):
                    for j in range(iw):
                        #若在边界
                        if i-bh<0 or i+bh>ih-1 or j-bw<0 or j+bw>iw-1 :
                            tF=getFmid(F,ih,iw,i,j,)
                            s=(Y[i:i+fh,j:j+fw]*tF).sum()
                        else:
                            s=(Y[i:i+fh,j:j+fw]*F).sum()
                        O[i][j] = s
#    O=O.clip(0,255)
    return O.astype(np.float64)

def getim():
    m=4
    n=4
    t=np.zeros((m,n)).astype('uint8')
    for i in range(m):
        for j in range(n):
            t[i][j]=i+j
#            if i == int(m/2):
#                t[i][j]=127
#            else:
#                t[i][j]=30
    print(t)
    return t

if __name__=='__main__':
    path='C:/Users/19041/Desktop/图像处理/图像处理作业/图像处理练习3/'
    im=imageio.imread(path+'1.jpg')
    F1=np.array(    
                [
                [1/4,1/4],
                [1/4,1/4]
                ]
                )
    F2=np.array(
                [
                [1/9,1/9,1/9],
                [1/9,1/9,1/9],
                [1/9,1/9,1/9]
                ]
                )
    F3=np.array(
                [
                [-1/8,-1/8,-1/8],
                [-1/8,1,-1/8],
                [-1/8,-1/8,-1/8]
                ]
                )
    F4=np.array(
            [
            [-1,-1,-1],
            [-1, 8,-1],
            [-1,-1,-1]
            ]
            )
    F=F2#调整这里选择核
    #im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)#控制转变为灰度图
    #im=getim()#调整这里获得构造图像
    show(im)
    #opencv
#    tcv=cv2.filter2D(im,-1,F)
#    print('cv2:')
    #print(tcv)
#    show(tcv)
    #我的程序
    way=2#调整这里选择边缘处理方式，默认为第二种
    t=Convolve(im,F,way)
    #print(t.shape)
    print('my')
    #print(t)
    show(t)
    print('相减')
#    show(t-tcv)
    #保存
    iname='1_'+str(way)+'.jpg'
    imageio.imwrite(path+iname,t)
    inamecv='1_'+'cv.jpg'
#    imageio.imwrite(path+inamecv,tcv)