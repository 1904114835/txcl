import matplotlib.pyplot as plt
import rotate
import math

xy=[[],[]]
n=3
for i in range(n):
    for j in range(n):
        xy[0].append(i)
    for j in range(n):
        xy[1].append(j)
xy1=rotate.rotate(xy,-30)

maxx=math.ceil( max(xy1[0]) )
maxy=math.ceil( max(xy1[1]) )
minx=math.floor( min(xy1[0]) )
miny=math.floor( min(xy1[1]) )

xy=[[],[]]

for i in range(minx-1,maxx+1):
    for j in range(miny-1,maxy+1):
        xy[0].append(i)
    for j in range(miny-1,maxy+1):
        xy[1].append(j)

plt.plot(xy[0],xy[1], 'o',color='b')
plt.plot(xy1[0],xy1[1],'o',color='r')

#mx=20
#plt.plot([-mx,mx],[-mx,mx],'o',color='w')
plt.show()