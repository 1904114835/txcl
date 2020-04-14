import numpy as np
import imageio 
import rotate
import scipy.interpolate
import matplotlib.pyplot as plt
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
def rotate_image(im,angle):
    h=im.shape[0]
    w=im.shape[1]
    midx=(w-1)/2
    midy=(h-1)/2
    max_h=-np.Infinity
    max_w=-np.Infinity
    total_point=h*w
    t_xy=np.zeros((2,total_point))
    values=np.zeros((w*h,3))
    #获取t_yx和values
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            t_xy[0][i*w +j]=j-midx#i,j与x，y坐标的换算
            t_xy[1][i*w +j]=midy-i
            values[i*w+j]=im[i][j]
    #np.arctan(h/w)/np.pi*180 测试左上角点是否旋转至水平
    t_xy=rotate.rotate(t_xy,angle)
    #获取边界
    for i in range(len(t_xy[0])):
        if t_xy[0][i]>max_w:
            max_w=t_xy[0][i]
        if t_xy[1][i]>max_h:
            max_h=t_xy[1][i]
    #矩阵转置
    t_xy=np.transpose(t_xy)
    #新图像大小
    new_h=int(max_h*2+1)
    new_w=int(max_w*2+1)
    new_im=np.zeros((new_h,new_w,3))
    new_h=new_im.shape[0]
    new_w=new_im.shape[1]
    new_midx=(new_w-1)/2
    new_midy=(new_h-1)/2
    #获取网格点
    xi=np.zeros((new_h*new_w,2))
    for i in range(new_im.shape[0]):
        for j in range(new_im.shape[1]):
            xi[i*new_w +j][0]=j-new_midx#i,j与x，y坐标的换算
            xi[i*new_w +j][1]=new_midy-i
    #使用scipy函数griddata实现，t_xy代表新的点的坐标，values代表点的值，xi是网格点的坐标
    new_im_values=scipy.interpolate.griddata(t_xy, values, xi)
    for i in range(new_im.shape[0]):
        for j in range(new_im.shape[1]):
            new_im[i][j]=new_im_values[i*new_w+j]
    return new_im.astype('uint8')

def show(im):
    plt.ion() 
    plt.imshow(im)
    plt.show()
    
def main(path):
    im=imageio.imread(path)
    show(im)
    angle=1414141
    im=rotate_image(im,angle)
    str_list = list(path)
    str_list.insert(-4,str(angle))
    tpath = ''.join(str_list)
    imageio.imwrite(tpath,im)
    show(im)

if __name__ == '__main__':
    main('C:/Users/19041/Desktop/im_Image Processing/crooked_horizon.jpg')
