import matplotlib.pyplot as plt
import imageio
import numpy as np
def show(im):
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

def Convolve(I,F,t=1,iw=0,ih=0,fw=0,fh=0):
    ih,iw = I.shape
    fh,fw = F.shape
    Y = np.zeros((ih+fh-1, iw+fw-1))
    T = np.zeros((ih, iw))
    Y[0:ih,fw-1:iw+fw-1]=I
    #置零法，不做处理
    if t==1:
        pass
    #对称法
    if t==2:
        Y[ih:ih+fh-1,fw-1:iw+fw-1]=Y[ih-fh+1:ih,fw-1:iw+fw-1]
        Y[0:ih,0:fw-1]=Y[0:ih,fw-1:2*fw-2]
    #加权法
    if t==3:
        #这个是加权方法的地方或许要修改F我写不动了
        pass
    #右上角对齐
    for i in range(T.shape[0]):
        for j in range(T.shape[1]):
            s=0
            for ti in range(fh):
                for tj in range(fw):
                    s+=Y[i+ti][j-tj]*F[ti][tj]
            T[i, j] = s 
    return (T.astype(np.uint8))
    
if __name__ == "__main__":
    I = imageio.imread('CARTOON.jpg')
    show(I)
    F = np.array([
        [1/4,1/4],
        [1/4,1/4]
    ])
    F2=np.array(
            [[1/9,1/9,1/9]
            ,[1/9,1/9,1/9]
            ,[1/9,1/9,1/9]
                    ])
    t=Convolve(I,F2,2)
    show(t)
    imageio.imwrite('a.jpg',t)



