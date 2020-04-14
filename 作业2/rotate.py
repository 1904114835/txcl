import numpy as np
def rotate(mat,degree):
    degree=360-degree
    rad=degree/180*np.pi
    ex=np.array([[np.cos(rad),np.sin(rad)],[-np.sin(rad),np.cos(rad)]])
    rotated=np.matmul(ex, mat)
    return rotated

if __name__=="__main__":
    mat=(np.random.rand(2,5)*100).astype('int')
    angle=-36.3523
    rotated=rotate(mat,angle)
    print('角度:',angle,'\n','原矩阵:\n',mat,'\n','旋转后矩阵:\n',rotated)
    
    
    
    
