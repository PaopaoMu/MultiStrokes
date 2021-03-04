import Pretreatment
import math

def turning_point(Temp):#记录折点
    A=[]
    B=[]
    A.append(Temp[0])
    A.append(Temp[len(Temp)-1])
    while A:
        p1=Temp.index(A[0])
        p2=Temp.index(A[1])
        temp=Temp[p1:p2+1]
        p_max=curve_change_line(A[0],A[1],temp,0.05)
        if p_max:
            A.insert(1, p_max)
        else:
            B.append(A[0])
            del A[0]
        if len(A)==1:
            B.append(A[0])
            del A[0]
            break
    # print("折点：",B)
    return B

def turning_point1(Temp):
    A=[]
    A.append(Temp[0])
    A.append(Temp[len(Temp)-1])
    j=0
    while j<len(A)-1:
        p1=A[j]
        p2=A[j+1]
        site1=Temp.index(p1)
        site2=Temp.index(p2)
        temp = Temp[site1:site2 + 1]
        if len(temp)<6:
            j+=1
        else:
            p_max = curve_change_line(p1,p2,temp,0.075)
            if p_max:
                A.insert(j+1,p_max)
                j = 0
                # break
            else:
                j+=1
    # print("折点：",A)
    return A


def curve_change_line(point1,point2,line,t):#折线化
    d=0
    x_max=0
    y_max=0
    line_d=Pretreatment.distance(point1[0],point1[1],point2[0],point2[1])
    # print(line)
    for each in line:
        dis=getDis(each[0],each[1],point1[0],point1[1],point2[0],point2[1])
        if dis>=d:
            d=dis
            x_max=each[0]
            y_max=each[1]
    if d>t*line_d:
        point_max=[x_max,y_max]
    else:
        point_max=[]
    return point_max


def getDis(pointX, pointY, lineX1, lineY1, lineX2, lineY2):#点到线段的距离
    # print(pointX, pointY, lineX1, lineY1, lineX2, lineY2)
    a = lineY2 - lineY1
    b = lineX1 - lineX2
    c = lineX2 * lineY1 - lineX1 * lineY2
    # print("a,b,c",a,b,c)
    dis = (math.fabs(a * pointX + b * pointY + c)) / (math.pow(a * a + b * b, 0.5))
    return dis

