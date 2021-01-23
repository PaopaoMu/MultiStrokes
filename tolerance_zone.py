import break_point
import numpy as np
import Pretreatment
import math


def is_overdraw(max_temp,min_temp):#判断是否重叠
    l=the_lengthest(max_temp)
    max_corpoint=break_point.turning_point(max_temp)#折线化的点
    temp1 = []  # 短笔画落入重叠区域的采样点
    for i in range(1,len(max_corpoint)):
        f_point=max_corpoint[i-1]
        b_point=max_corpoint[i]
        R,T=coordinate_transformation(f_point,b_point)
        length=Pretreatment.distance(f_point[0],f_point[1],b_point[0],b_point[1])
        x=length/2#容差长度范围
        y = 3 / 4 * float('%.2f' % (length ** 0.5)) + 2  # 找到容差宽度
        h=0
        while h<len(min_temp):
            X=np.array([min_temp[h][0],min_temp[h][1],1])
            Y=R@T@X
            r1 = ((min_temp[h][0] - f_point[0]) ** 2 + (min_temp[h][1] - f_point[1]) ** 2)
            r2 = ((min_temp[h][0] - b_point[0]) ** 2 + (min_temp[h][1] - b_point[1]) ** 2)
            if math.fabs(Y[0])<=x and math.fabs(Y[1])<=y or r1<=y*y or r2<=y*y:
                if min_temp[h] in temp1:
                    pass
                else:
                    a=min_temp[h]
                    temp1.append(a)
            h+=1
    k=len(temp1)/len(min_temp)
    return temp1,k




def coordinate_transformation(a,b):#求坐标变换矩阵
    m=[(a[0]+b[0])/2,(a[1]+b[1])/2]
    T=np.array([[1,0,-m[0]],[0,1,-m[1]],[0,0,1]])
    x=b[0]-m[0]
    y=b[1]-m[1]
    ux = x / ((x ** 2 + y ** 2) ** 0.5)
    uy = y / ((x ** 2 + y ** 2) ** 0.5)
    R=np.array([[ux,uy,0],[-uy,ux,0],[0,0,1]])
    return R,T


def the_lengthest(temp):#最大的弦长笔画
    s1=temp[0]
    d_max=0
    for i in range(1,len(temp)):
        s2=temp[i]
        d=Pretreatment.distance(s1[0],s1[1],s2[0],s2[1])
        if d>d_max:
            d_max=d
    return d_max


def line_length(temp):
    l=0
    for i in range(1,len(temp)):
        a=temp[i-1]
        b=temp[i]
        d=Pretreatment.distance(a[0],a[1],b[0],b[1])
        l=l+d
    return l

