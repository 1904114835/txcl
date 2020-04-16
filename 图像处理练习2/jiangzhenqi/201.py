import imageio	 #用来做图像读写
import matplotlib.pyplot as plt	#用来显示图像
import numpy as np
import math
from scipy.interpolate import griddata

path_work = 'C:/Users/19041/Desktop/'
file_in = path_work+'crooked_horizon.jpg'
file_out = path_work+'dust.jpg'

#读入图像
im = imageio.imread(file_in)

#显示图像
def show(im):
    plt.ion() 
    plt.imshow(im)
    plt.show()
    plt.close()
    
show(im)
inp = im   # 输入图像
a = inp.shape
input_row = a[0]
input_col = a[1]# 输入图像的尺寸（行、列）

angle = 30*math.pi/180
cosa = math.cos(angle)
sina = math.sin(angle)

maxx=0
maxy=0
minx=9999
miny=9999
xy=np.zeros((input_row*input_col,2))
values=np.zeros((input_row*input_col,3))
h=input_row
w=input_col

for i in range(input_row):
    for j in range(input_col):
        x = int(cosa*i-sina*j-0.5*input_col*cosa+0.5*input_row*sina+0.5*input_col)
        y = int(sina*i+cosa*j-0.5*input_col*sina-0.5*input_row*cosa+0.5*input_row)
        if i==0 and j==0:
            print(x,y,inp[i,j])
        xy[i*w+h]=[x,y]
        values[i*w+h]=inp[i,j]
        if x>maxx:
            maxx=x
        if y>maxy:
            maxy=y
        if x<minx:
            minx=x
        if y<miny:
            miny=y
            
print(maxx,maxy,minx,miny)
print(xy.shape,values.shape)


grid=np.zeros((maxx*maxy,2))
for i in range(maxx):
    for j in range(maxy):
        grid[i*maxx +j][0]=j-(maxx-minx)/2
        grid[i*maxx +j][1]=(maxy-miny)/2-i
        
newim=np.zeros((maxx-minx,maxy-miny,3))
output1 = griddata(xy, values, grid)

for i in range(maxx):
    for j in range(maxy):
        newim[i,j]=output1[i*maxy+j]
show(newim)
# 保存生成结果
#imageio.imwrite(file_out, output1)

pause=1; 