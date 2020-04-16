# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:40:32 2020

@author: Feather
"""

import numpy as np
import math
import imageio #用来做图像读写
import matplotlib.pyplot as plt  #用来显示图像
def Imresize(picture , n ):
    '''
    双线性插值函数 参数说明
    picture: 输入图像
    n: 放大倍数
    return: 双线性插值后的图像
    '''
    #输入图像的副本

    #输入图像的尺寸（行、列）
    input_row, input_col = picture.shape

    #输出图像的尺寸
    output_row = int(input_row * n)
    output_col = int(input_col * n)

    #初始化输出图片（赋予零灰度值）
    output = np.zeros((output_row, output_col))
    temp=[]
    for i in range(output_row):
        for j in range(output_col):
            
            #输出图片中坐标 （i，j）对应至输入图片中的（x,y）
            x = i / n
            y = j / n
            
            #求距 (x, y) 点最近的四个点（x1，y1）（x2, y2），（x3， y3），(x4，y4)
            x1 = int(x)
            y1 = int(y)

            x2 = x1
            y2 = y1 + 1

            x3 = x1 + 1
            y3 = y1

            x4 = x1 + 1
            y4 = y1 + 1
            
            #求双线性插值公式中的u，v
            a = x - x1
            b = y - y1
            ''''''
            #边界值处理，防止越界
            if x4 >= input_row:
                x4 = input_row - 1
                x3 = x4
                x1 = x4 - 1
                x2 = x4 - 1
            if y4 >= input_col:
                y4 = input_col - 1
                y2 = y4
                y1 = y4 - 1
                y3 = y4 - 1
            
            # 插值
            output[i][j] =(1-a)*(1-b)*(picture[x1][y1])+ (a)*(1-b)*(picture[x2][y2])+ (1-a)*(b)*(picture[x3][y3])+ a*b*picture[x4][y4]
    return output.astype('uint8')

def show(im):
    plt.imshow(im,cmap="gray")
    plt.show()
    plt.close()
def main():
    #图像路径信息
    path_work = 'C:/Users/19041/Desktop/图像处理/图像处理练习1 - 副本/'
    file_in1 = path_work+'CARTOON.jpg'
    file_in2 = path_work+'flowergray.jpg'
    file_out1 = path_work+'CARTOON_Small.jpg'
    file_out2 = path_work+'CARTOON_Large.jpg'
    file_out3 = path_work+'flowergray_Small.jpg'
    file_out4 = path_work+'flowergray_Large.jpg'
    
    show([[0,0.5],[0.75,1]])
    #读入图像,进行双线性插值处理并保存处理后的图像
    im1 = imageio.imread(file_in1)
    out1=Imresize(im1,0.75)
    imageio.imwrite(file_out1, out1)
    out2=Imresize(im1,1.5)
    imageio.imwrite(file_out2, out2)
    
    show(im1)
    show(out1)
    show(out2)
    
    im2 = imageio.imread(file_in2)
    out3=Imresize(im2,0.75)
    imageio.imwrite(file_out3, out3)
    out4=Imresize(im2,1.5)
    imageio.imwrite(file_out4, out4)
    show(im2)
    show(out3)
    show(out4)

if __name__ == '__main__':
    main()