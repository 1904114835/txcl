import my_match
import cv2

# 读取拼接图片
imageA = cv2.imread("left_01.png")
imageA = cv2.cvtColor(imageA,cv2.COLOR_BGR2GRAY)
imageB = cv2.imread("right_01.png")
imageB = cv2.cvtColor(imageB,cv2.COLOR_BGR2GRAY)



# 把图片拼接成全景图
match_class = my_match.my_match()

match_class.show(imageA)
match_class.show(imageB)


(result,match_pic) = match_class.joint([imageA, imageB])

# 显示所有图片
match_class.show(match_pic)
match_class.show(result)