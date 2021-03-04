import numpy as np
import math

#去除噪音点
def deletion(arr):
    n=10
    m=15
    length1=len(arr)
    num=[]
    for j in arr:
        l=len(j)
        num.append(l)
    for i in range(length1):
        length= 0
        num1=num[i]
        if num1==1:
            num[i]=0
        if num1<=n and num1!=0:
            temp=arr[i]
            for j in range(1,num1):
                length2=distance(temp[j-1][0],temp[j-1][1],temp[j][0],temp[j][1])
                length+=length2
            if length<=m:
                arr[i].clear()
                num[i]=0
    temp=filter(lambda x:x!=0,num)#得到数组中不为零的元素
    new_num1=list(temp)
    arr1=[x for x in arr if x]
    # print("去噪：",arr1)
    return arr1

# 对每一笔进行重采样
def renew_process(arr):
    Dis = 0
    temp = []
    temp = arr
    rs = []
    mbrd = Outer_rectangle(temp)
    s = mbrd * 0.01
    rs.append(temp[0])
    for i in range(1, len(temp) - 1):
        d = distance(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1])
        if Dis + d > s:
            m_x = temp[i][0] + (s - d) * (temp[i][0] - temp[i - 1][0]) / d
            m_y = temp[i][1] + (s - d) * (temp[i][1] - temp[i - 1][1]) / d
            a = [int(m_x), int(m_y)]
            rs.append(a)
            Dis = 0
        else:
            Dis += d
        if i == len(temp) - 1:
            rs.append([temp[i][0], temp[i][1]])
    # print("重采样：",rs)
    return rs

#笔画平滑
def smooth(arr):
    temp = []
    temp.append(arr[0])
    for i in range(1, len(arr) - 2):
        p_x = (arr[i - 1][0] + 3 * arr[i][0] + arr[i + 1][0]) / 5
        p_y = (arr[i - 1][1] + 3 * arr[i][1] + arr[i + 1][1]) / 5
        a = [p_x, p_y]
        temp.append(a)
    temp.append(arr[len(arr) - 1])
    # print("平滑后：",temp)
    return temp

def head(temp):#去头
    length1=0
    mbrd_length=int(Outer_rectangle(temp))
    L=mbrd_length*0.1
    for i in range(1,len(temp)):
        length2=distance(temp[i-1][0],temp[i-1][1],temp[i][0],temp[i][1])
        length1+=length2
        if length1>L:
            i-=1
            break
    for j in range(1,i-1):
        R=calculate_curve2(temp[j-1][0],temp[j][0],temp[j+1][0],temp[j-1][1],temp[j][1],temp[j+1][1])
        R1 = np.round(R, 5)
        if R1>=0.5:
            for m in range(j):
                temp[m].clear()
    temp1= [x for x in temp if x]
    print("去头:",temp1)
    return temp1

def tail(temp):#去尾
    length1=0
    mbrd_length=int(Outer_rectangle(temp))
    L=mbrd_length*0.1
    for i in range(len(temp)-2,0,-1):
        length2=distance(temp[i-1][0],temp[i-1][1],temp[i][0],temp[i][1])
        length1+=length2
        if length1>L:
            i-=1
            break
    for j in range(len(temp)-2,i,-1):
        R=calculate_curve2(temp[j-1][0],temp[j][0],temp[j+1][0],temp[j-1][1],temp[j][1],temp[j+1][1])
        R1=np.round(R,5)
        if R1>=0.6:
            for m in range(len(temp)-1,j,-1):
                temp[m].clear()
    temp1= [x for x in temp if x]
    print ("去尾后：",temp1)
    return temp1

def merge_h_t(arr):#对头尾坐标距离较小的两点进行合并
    temp1=arr[0]
    temp2=arr[len(arr)-1]
    length=distance(temp1[0],temp1[1],temp2[0],temp2[1])
    print("头尾长度：",length)
    if length<20:
        temp_x=(temp1[0]+temp2[0])/2
        temp_y=(temp1[1]+temp2[1])/2
        a=[temp_x,temp_y]
        arr.insert(0,a)
        arr.append(a)
    print("闭合：",arr)
    return arr

def distance(x1,y1,x2,y2):#两点之间的距离
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def Outer_rectangle(temp):#最小外包矩形
    list_x=[]
    list_y=[]
    for i in range(len(temp)):
        a=temp[i][0]
        b=temp[i][1]
        list_x.append(a)
        list_y.append(b)
    max_x=max(list_x)
    max_y=max(list_y)
    min_x=min(list_x)
    min_y=min(list_y)
    a=[min_x,max_y,max_x,min_y]
    diagonal_length=distance(min_x,max_y,max_x,min_y)
    return diagonal_length

def calculate_curve2(x1,x2,x3,y1,y2,y3):#计算曲率
    d1=distance(x1,y1,x2,y2)
    d2=distance(x2,y2,x3,y3)
    a1=math.asin((y2-y1)/d1)
    a2=math.asin((y3-y2)/d2)
    re_a=abs(a2-a1)
    k=re_a/(d1+d2)
    return k


def Outer_rect(temp):#最小外包矩形
    list_x=[]
    list_y=[]
    for i in range(len(temp)):
        a=temp[i][0]
        b=temp[i][1]
        list_x.append(a)
        list_y.append(b)
    max_x=max(list_x)
    max_y=max(list_y)
    min_x=min(list_x)
    min_y=min(list_y)
    return max_x,max_y,min_x,min_y