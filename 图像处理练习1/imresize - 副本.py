import numpy 
import imageio
import datetime
import matplotlib.pyplot as plt
import cv2
import imresize
tab=[[] for i in range(1005)]
def Imresize(ori_im, ori_size, tar_size):
    tar_im=numpy.zeros(tar_size)
    ratio_i=tar_size[0]/ori_size[0]
    ratio_j=tar_size[1]/ori_size[1]
    h=tar_size[0]
    w=tar_size[1]
    for i in range(h):
        for j in range(w):
            ori_i=i/ratio_i
            ori_j=j/ratio_j
            x1=int(ori_i)
            y1=int(ori_j)
            if x1==ori_i and y1==ori_j:
                tar_im[i][j]=ori_im[x1][y1]
                continue
            if x1==ori_size[0]-1:
                x2=x1
            else:
                x2=x1+1
            if y1==ori_size[1]-1:
                y2=y1
            else:
                y2=y1+1
            b=ori_i-x1
            a=ori_j-y1
            _b=int((1-b)*1000)
            _a=int((1-a)*1000)
            a=int(a*1000)
            b=int(b*1000)
            t1=tab[_a][ori_im[x1][y1]]#v1*(1-a)
            t2=tab[a][ori_im[x1][y2]]#av2
            t3=tab[_a][ori_im[x2][y1]]#(1-a)v3
            t4=tab[a][ori_im[x2][y2]]#av4
            tar_im[i][j]=tab[_b][t1]+tab[_b][t2]+tab[b][t3]+tab[b][t4]
    return tar_im.astype('uint8')

def show(im):
    plt.imshow(im,cmap="gray")
    plt.show()
    plt.close()

def main(path_work,num_im,big_ratio,small_ratio,*arg):
    for i in range(num_im):
        im = imageio.imread(path_work+eval("arg["+str(i)+"]"))
        ori_size=im.shape
        out_im=Imresize(im,ori_size,[int(ori_size[0]*big_ratio),int(ori_size[1]*big_ratio)])
        imageio.imwrite(path_work+"out_big_"+eval("arg["+str(i)+"]"), out_im)
    
        start = datetime.datetime.now()    
        out_im=Imresize(im,ori_size,[int(ori_size[0]*small_ratio),int(ori_size[1]*small_ratio)])
        end = datetime.datetime.now()
        print ("my",end-start)
        
        imageio.imwrite(path_work+"out_small_"+eval("arg["+str(i)+"]"), out_im)
    
#    show((out_im-imresize.imresize(im,ori_size,[int(ori_size[0]*small_ratio),int(ori_size[1]*small_ratio)])))
#    show(1-imresize.imresize(im,ori_size,[int(ori_size[0]*small_ratio),int(ori_size[1]*small_ratio)])-\
#         cv2.resize(im,tuple([int(ori_size[0]*small_ratio),int(ori_size[1]*small_ratio)]), 
#                    interpolation = cv2.INTER_CUBIC))
#    
    start = datetime.datetime.now()
    resized=cv2.resize(im,(int(ori_size[0]*small_ratio),int(ori_size[1]*small_ratio)), interpolation = cv2.INTER_CUBIC)
    end = datetime.datetime.now()
    print ("cv",end-start)
    
    show(1-out_im+resized)
    
if __name__ == '__main__':
    start = datetime.datetime.now()
    for i in range(len(tab)):
        for j in range(260):
            tab[i].append(int(i*j/1000))
    main('C:/Users/19041/Desktop/图像处理/图像处理练习1/',2,1.5,0.75,'CARTOON.jpg','flowergray.jpg')
    end = datetime.datetime.now()
    print (end-start)