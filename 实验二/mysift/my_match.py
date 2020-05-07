import numpy as np
import cv2
import matplotlib.pyplot as plt
import newsift as mysift
import copy
import conv
class my_match:
    def show_im_and_kp(self,im,kp):
            tim=copy.deepcopy(im)
            for i in range(len(kp)):
                tim[int(kp[i][1])][int(kp[i][0])]=255
            conv.show(tim)
    #拼接函数
    def joint(self, images, top_v=0.8, reprojThresh=4.0,get_Matches=True):
        (imageB, imageA) = images
        
        '''
        descriptor = cv2.xfeatures2d.SIFT_create()
        # 检测SIFT特征点，并计算描述子
        (kpsA, featuresA) = descriptor.detectAndCompute(imageA, None)
        kpsA=np.float32([i.pt for i in kpsA])
        
        print(type(kpsA),type(featuresA))
        
        print(kpsA.shape,featuresA.shape)
        print(featuresA[0])
#        for i in range(100):
#            print(kpsA[i])
        
        (kpsB, featuresB) = descriptor.detectAndCompute(imageB, None)
        kpsB=np.float32([i.pt for i in kpsB])
        
        print(kpsB.shape,featuresB.shape)
#        print(featuresA[0])
        
        del descriptor
        '''
        descriptor = mysift.my_sift()
        kpsA,featuresA=descriptor.get_kp_and_feature(imageA)
        kpsA=np.array(kpsA)
        featuresA=np.array(featuresA).astype('float32')
        print("kp and features of A OK")
#        print(type(kpsA),type(featuresA))
#        print(kpsA.shape,featuresA.shape)
#        print(featuresA[0])

        descriptor.show_im_and_kp()
        del descriptor
        descriptor = mysift.my_sift()
        kpsB,featuresB=descriptor.get_kp_and_feature(imageB)
        print("kp and features of B OK")
        kpsB=np.array(kpsB)
        featuresB=np.array(featuresB).astype('float32')
        descriptor.show_im_and_kp()
        del descriptor
        
        for i in range(len(kpsA)):
            t=kpsA[i][0]
            kpsA[i][0]=kpsA[i][1]
            kpsA[i][1]=t
        for i in range(len(kpsB)):
            t=kpsB[i][0]
            kpsB[i][0]=kpsB[i][1]
            kpsB[i][1]=t
        self.show_im_and_kp(imageA,kpsA)
        self.show_im_and_kp(imageB,kpsB)
        
        # 匹配两张图片的所有特征点，返回匹配结果
        matcher = cv2.BFMatcher()
  
        # 使用KNN检测来自A、B图的SIFT特征匹配对，K=2
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        print(np.shape(rawMatches))
        matches = []
        for m in rawMatches:
            # 当最近距离跟次近距离的比值小于ratio值时，保留此匹配对
            if len(m) == 2 and m[0].distance < m[1].distance * top_v:
            # 存储两个点在featuresA, featuresB中的索引值
                matches.append((m[0].trainIdx, m[0].queryIdx))
        
        print(np.shape(matches))
        if len(matches) > 4:
            # 获取匹配对的点坐标
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])

            # 计算视角变换矩阵
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)
#        print(H)
        if len(H)==0 or len(status)==0 or len(matches)==0:
            return None
        # 否则，提取匹配结果
        # H是3x3视角变换矩阵      
        # 将图片A进行视角变换，result是变换后图片
        rwide=imageA.shape[1]+imageB.shape[1]
        rhigh=imageA.shape[0]
#        print(rwide,rhigh)
        result = cv2.warpPerspective(imageA, H, (rwide,rhigh) )
#        self.show(result)
        # 将图片B传入result图片最左端
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
#        self.show(result)
        # 检测是否需要显示图片匹配
        if get_Matches:
            # 生成匹配图片
            match_pic = self.draw_match_lines(imageA, imageB, kpsA, kpsB, matches, status)
            # 返回结果
            return (result,match_pic)

        # 返回匹配结果
        return result
    def show(self,im):
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


    def draw_match_lines(self, imageA, imageB, kpsA, kpsB, matches, status):
#        print(status)
        hA, wA = imageA.shape[:2]
        hB, wB = imageB.shape[:2]
#        print((hA, wA),(hB, wB))
        if len(np.shape(imageA))==3:
            match_pic= np.zeros((max(hA,hB), wA + wB,3)).astype("uint8")
        else:
            match_pic= np.zeros((max(hA,hB), wA + wB)).astype("uint8")
        
        match_pic[0:hA, 0:wA] = imageA
        match_pic[0:hB, wA-1:-1] = imageB

        # 联合遍历，画出匹配对
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # 当点对匹配成功时，画到可视化图上
            if s == 1:
                # 画出匹配对
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(match_pic, ptA, ptB, (255, 255, 255), 1)

        # 返回可视化结果
        return match_pic