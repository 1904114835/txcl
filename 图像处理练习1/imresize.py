import numpy 
import imageio 

def imresize(ori_im, ori_size, tar_size):
    tar_im=numpy.zeros(tar_size)
    ratio_i=tar_size[0]/ori_size[0]
    ratio_j=tar_size[1]/ori_size[1]
    for i in range(len(tar_im)):
        for j in range(len(tar_im[i])):
            ori_i=i/ratio_i
            ori_j=j/ratio_j
            x1=int(ori_i)
            y1=int(ori_j)
            if x1==ori_i and y1==ori_j:
                tar_im[i][j]=ori_im[x1][y1]
                continue
            b=ori_i-x1
            a=ori_j-y1
            t1=(1-a)*(1-b)*ori_im[x1][y1]
            t2=a*(1-b)*ori_im[x1][y1] if y1+1>=ori_size[1] else a*(1-b)*ori_im[x1][y1+1]
            t3=(1-a)*b*ori_im[x1][y1] if x1+1>=ori_size[0] else (1-a)*b*ori_im[x1+1][y1]
            t4=a*b*ori_im[x1][y1] if x1+1>=ori_size[0] or y1+1>=ori_size[1] else a*b*ori_im[x1+1][y1+1]
            tar_im[i][j]=t1+t2+t3+t4
    return tar_im.astype('uint8')

def main(path_work,num_im,big_ratio,small_ratio,*arg):
    for i in range(num_im):
        im = imageio.imread(path_work+eval("arg["+str(i)+"]"))
        ori_size=im.shape
        out_im=imresize(im,ori_size,[int(ori_size[0]*big_ratio),int(ori_size[1]*big_ratio)])
        imageio.imwrite(path_work+"out_big_"+eval("arg["+str(i)+"]"), out_im)
        out_im=imresize(im,ori_size,[int(ori_size[0]*small_ratio),int(ori_size[1]*small_ratio)])
        imageio.imwrite(path_work+"out_small_"+eval("arg["+str(i)+"]"), out_im)
    
if __name__ == '__main__':
    main('C:/Users/19041/Desktop/图像处理/图像处理练习1/',2,1.5,0.75,'CARTOON.jpg','flowergray.jpg')