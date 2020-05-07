import numpy as np
import rotate_image
import cv2
def get_M_Theta(I,sigma) :
#    print(np.average(I))
    I = np.pad(I,1, 'constant')
    #print(I)
    A=I[1:I.shape[0]-1, :I.shape[1]-2]
    #print(A)
    B=I[1:I.shape[0]-1,2:I.shape[1]]
    #print(B)
    C=I[:I.shape[0]-2,1:I.shape[1]-1]
    #print(C)
    D=I[2:I.shape[0],1:I.shape[1]-1]
    #print(D)
    x =np.linspace(int(-I.shape[0]/2),int(I.shape[0]/2) ,I.shape[0]-2)
    y =np.linspace(int(-I.shape[1]/2),int(I.shape[1]/2),I.shape[1]-2)
    X,Y = np.meshgrid(x, y)
    ans=np.exp(-(X**2+Y**2)/ (2*sigma*sigma))/ (2*np.pi*sigma)
    ans=ans/ans.sum( )
    M=np.sqrt((B-A)**2+(D-C)**2)#*ans
#    print(np.average(M))
    #Theta=2*np.arctan(()/())*180/np.pi
    Theta=np.arctan2(D-C,B-A)*180/np.pi
    #print (Theta)
    return M, Theta

def main_direction(Theta) :
    hist,bins = np.histogram(Theta,bins = [-180, -135,-90, -45,0,45, 90,135,180] )
    other_hist=hist.copy().astype( 'float') 
    for i in range(1, len(other_hist)-1) :
        other_hist[i]=0.25*hist[i-1]+0.5*hist[i]+0.25*hist[i+1]
#    print( 'hist' ,hist)
#    print( 'other_hist' ,other_hist)
    index=np.argmax (other_hist)
    c=Theta*( (bins[index] < Theta) & (Theta < bins [index+1]))
    avg=c.sum() /hist[index]
    return avg

def get_feature(detect,zu):
    sigma=1.6*2**zu
#    print(np.average(detect),detect.shape)
    d=4
    nowi=int(detect.shape[0]/2)
    nowj=int(detect.shape[1]/2)
    d=int(min(detect.shape)/4)
    M,theta=get_M_Theta(detect[nowi-d:nowi+d,nowj-d:nowj+d],sigma)
    
#    print(M,theta)
    maintheta=main_direction(theta)
    if maintheta<0:
        maintheta+=360
    vec=[]
    tim=rotate_image.rotate_image(detect,maintheta)
    midi=int(tim.shape[0]/2)
    midj=int(tim.shape[1]/2)
    
    for jx in range(min(midi,midj)):
        if tim[midi-jx][midj-jx]==0 and tim[midi-jx][midj+jx]==0 and tim[midi+jx][midj-jx]==0 and tim[midi+jx][midj+jx]==0:
            jx=jx-1
            break
    tim=tim[midi-jx:midi+jx+1,midj-jx:midj+jx+1]
    shape=tim.shape
    tim=cv2.resize(tim, (4*shape[0], 4*shape[1]))
    shape=tim.shape
#    print(np.shape(tim))
    for i in range(4):
        for j in range(4):
            his=[0 for hisi in range(8)]
            M,theta=get_M_Theta(tim[int(shape[0]/4*i):int(shape[0]/4*(i+1)),int(shape[1]/4*j):int(shape[1]/4*(j+1))],sigma)
            for h in range(M.shape[0]):
                for k in range(M.shape[1]):
                    temp_theta=int(theta[h][k]/45)
                    if temp_theta<0:
                        temp_theta+=360
#                    print(temp_theta)
                    his[ temp_theta ]+=M[h][k]
            for t in his:
                vec.append(t)
            
    
    return vec
                
            
    
def get_keypoints(dog,g_pyr,r=10):  
    kp=[]
    feature=[]
    for zu in range(np.shape(dog)[0]):
        #这里的temp是图像金字塔的一层的尺度图的组
        temp=np.array(dog[zu])
#        print(np.average(temp[0]))
        for pic in range(1,np.shape(dog)[1]-1):
            #对于一张图片里
            for i in range(1,dog[zu][pic].shape[0]-1):
                for j in range(1,dog[zu][pic].shape[1]-1):
                    D=temp[pic-1:pic+2,i-1:i+2,j-1:j+2]
                    avg=np.average(D)
#                    print(avg)
                    if dog[zu][pic][i][j]>1*avg:# and dog[zu][pic][i][j]>0.5:
                        tmax=D.max()
                        tmin=D.min()
                        if dog[zu][pic][i][j]==tmax or dog[zu][pic][i][j]==tmin:
                            rad=5
                            if rad+i+1<temp[pic].shape[0] and rad+j+1<temp[pic].shape[1] and i-rad>0 and j-rad>=0:  
                                detect=g_pyr[zu][pic][i-rad:i+rad+1,j-rad:j+rad+1]
                                vec=get_feature(detect,zu)
                                fi=int(i*2**(zu))
                                fj=int(j*2**(zu))
                                kp.append([fi,fj])
                                feature.append(vec)
                    
    return kp,feature