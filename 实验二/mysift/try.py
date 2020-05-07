# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 15:50:37 2020

@author: 19041
"""
import cv2
import pyr
import conv
import kp
import numpy as np
def describe_M_Theta(I,sigma) :
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
    x =np.linspace(int(-I.shape[0]/2) , int(I.shape[0]/2) ,I.shape[0]-2)
    y =np.linspace(int(-I.shape[1]/2),int(I.shape[1]/2),I.shape[1]-2)
    X,Y = np.meshgrid(x, y)
    ans=np.exp(- (X**2+Y**2)/ (2*sigma*sigma))/ (2*np.pi*sigma)
    ans=ans/ans.sum( )
    M=np.sqrt((B-A)**2+(D-C)**2)*ans
    #print(M)
    #Theta=2*np.arctan(()/())*180/np.pi
    Theta=np.arctan2(D-C,B-A)*180/np.pi
    #print (Theta)
    return M, Theta
def main_direction(Theta) :
    hist,bins = np.histogram(Theta,bins = [-180, -135,-90, -45,0,45, 90,135,180] )
    other_hist=hist.copy().astype( 'float') 
    for i in range(1, len(other_hist)-1) :
        other_hist[i]=0.25*hist[i-1]+0.5*hist[i]+0.25*hist[i+1]
    print( 'hist' ,hist)
    print( 'other_hist' ,other_hist)
    index=np.argmax (other_hist)
    c=Theta*( (bins[index] < Theta) & (Theta < bins [index+1]))
    avg=c.sum( ) /hist[index]
    return avg


t=np.zeros((16,16))

for i in range(t.shape[0]):
    for j in range(t.shape[1]):
        t[i][j]=(8-i)**2+(8-j)**2

imageA = cv2.imread("1.jpg").astype(np.uint8)
#imageA = cv2.imread("left_01.png")
imageA = cv2.cvtColor(imageA,cv2.COLOR_BGR2GRAY)
t=imageA
conv.show(t)
t=conv.Convolve(t,pyr.gskernel(5,10))
print(pyr.gskernel(5,10))
print(cv2.getGaussianKernel(5,10))
conv.show(t)

sigma=1.6
m,theta=describe_M_Theta(t,sigma)
print(m.shape,theta.shape)
print(m)
print(theta)

avg=main_direction(theta)


print(avg)








