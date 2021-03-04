import Pretreatment
import numpy as np
import tolerance_zone
import merge



def modify(temp1, temp2):  # 修改类笔画的融合
    point = overtrace_area2(temp1, temp2)
    a = temp1.index(point[0])
    b = temp1.index(point[1])
    c = temp2.index(point[2])
    d = temp2.index(point[3])
    # print("待修改区域", a, b, c, d)
    if a > b:
        t = b
        b = a
        a = t
    if c > d:
        t = d
        d = c
        c = t
    p1 = temp1[a:b + 1]
    p2 = temp2[c:d + 1]
    if the_direction_of_the_stroke(p1, p2):
        pass
    else:
        temp2.reverse()
    if a == 0 and c != 0:
        new_temp1 = temp2[0:c + 1]
        new_temp1 = Chord_weighting(new_temp1, temp1[a])
    elif a != 0 and c == 0:
        new_temp1 = temp1[0:a + 1]
        new_temp1 = Chord_weighting(new_temp1, temp2[c])
    else:
        new_temp1 = []
    if len(p1) > len(p2):
        m = len(p2)
        max_temp = p1
        min_temp = p2
    else:
        m = len(p1)
        max_temp = p2
        min_temp = p1
    i = 0
    j = 0
    ntemp = []
    while i < len(min_temp):
        l1 = (max_temp[j][0] - min_temp[i][0]) ** 2 + (max_temp[j][1] - min_temp[i][1]) ** 2
        while j < len(max_temp) - 1:
            j += 1
            l2 = (max_temp[j][0] - min_temp[i][0]) ** 2 + (max_temp[j][1] - min_temp[i][1]) ** 2
            if l2 < l1:
                l1 = l2
            else:
                break
        i += 1
        ntemp.append(max_temp[j - 1])
    new_temp2 = []
    for i in range(m):
        new_p = [(min_temp[i][0] + ntemp[i][0]) / 2, (min_temp[i][1] + ntemp[i][1]) / 2]
        new_temp2.append(new_p)
    if b == len(temp1) - 1 and d != len(temp2) - 1:
        new_temp3 = temp2[d + 1:len(temp2)]
        new_temp3.reverse()
        new_temp3 = Chord_weighting(new_temp3, temp1[b])
        new_temp3.reverse()
    elif b != len(temp1) - 1 and d == len(temp2) - 1:
        new_temp3 = temp1[b + 1:len(temp1)]
        new_temp3.reverse()
        new_temp3 = Chord_weighting(new_temp3, temp2[d])
        new_temp3.reverse()
    else:
        new_temp3 = []
    new_temp = new_temp1 + new_temp2 + new_temp3
    return new_temp


def extend(temp1, temp2):  # 延伸类笔画
    d1 = Pretreatment.distance(temp1[0][0], temp1[0][1], temp2[0][0], temp2[0][1])
    d2 = Pretreatment.distance(temp1[0][0], temp1[0][1], temp2[1][0], temp2[1][1])
    if d1 < d2:
        ftemp = temp1
        btemp = temp2
    else:
        ftemp = temp2
        btemp = temp1
    point = overtrace_area(ftemp, btemp)
    a = ftemp.index(point[0])
    b = ftemp.index(point[1])
    c = btemp.index(point[2])
    d = btemp.index(point[3])
    # print("a,b,c,d", a, b, c, d)
    if a > b:
        t = b
        b = a
        a = t
    if c > d:
        t = d
        d = c
        c = t
    # x = (point[0][0] + point[1][0] + point[2][0] + point[3][0]) / 4
    # y = (point[0][1] + point[1][1] + point[2][1] + point[3][1]) / 4
    # p1 = ftemp[a:b + 1]
    # p2 = btemp[c:d + 1]
    # # 找重叠区域的中点到两条笔画上最小距离的点
    # n = find_minpoint([x, y], p1)
    # m = find_minpoint([x, y], p2)
    # i = ftemp.index(n)
    # j = btemp.index(m)
    # ntemp1 = ftemp[0:i + 1]
    # ntemp2 = btemp[j:len(btemp)]
    # mx, my = (n[0] + m[0]) / 2, (n[1] + m[1]) / 2
    # new_temp1 = Chord_weighting(ntemp1, [mx, my])  # 弦长加权法求新的数据点
    # new_temp1.append([mx, my])
    # ntemp2.reverse()
    # new_temp2 = Chord_weighting(ntemp2, [mx, my])
    # new_temp2.reverse()
    # new_temp = new_temp1 + new_temp2
    new_temp = []
    for i in range(a + 1):
        new_temp.append(ftemp[i])
    Mtemp = btemp[c:d + 1]
    Mtemp.reverse()
    ntemp = Chord_weighting(Mtemp, point[0])
    i = len(ntemp) - 1
    while i >= 0:
        new_temp.append(ntemp[i])
        i -= 1
    for i in range(d, len(btemp)):
        new_temp.append(btemp[i])
    print("new_temp", new_temp)
    return new_temp



def general_equation(x1, y1, x2, y2):  # 求一般式Ax+By+C=0
    B = x1 - x2
    A = y2 - y1
    C = x2 * y1 - x1 * y2
    return A, B, C




def overtrace_area(temp1, temp2):  # 重叠区域
    d1 = Pretreatment.distance(temp1[0][0], temp1[0][1], temp2[0][0], temp2[0][1])
    d2 = Pretreatment.distance(temp1[0][0], temp1[0][1], temp2[1][0], temp2[1][1])
    if d1 < d2:
        c = temp2[0]
        a = find_minpoint(c, temp1)
    else:
        a = temp1[0]
        c = find_minpoint(a, temp2)
    d3 = Pretreatment.distance(temp1[len(temp1) - 1][0], temp1[len(temp1) - 1][1], temp2[len(temp2) - 1][0],
                                      temp2[len(temp2) - 1][1])
    d4 = Pretreatment.distance(temp1[len(temp1) - 1][0], temp1[len(temp1) - 1][1], temp2[len(temp2) - 2][0],
                                      temp2[len(temp2) - 2][1])
    if d3 > d4:
        b = temp1[len(temp1) - 1]
        d = find_minpoint(b, temp2)
    else:
        d = temp2[len(temp2) - 1]
        b = find_minpoint(d, temp1)
    temp = [a, b, c, d]
    # print("四个点：", temp)
    return temp


def find_minpoint(p, temp):  # 找到最近的点
    dis = (p[0] - temp[0][0]) ** 2 + (p[1] - temp[0][1]) ** 2
    min_point = temp[0]
    for i in range(1, len(temp)):
        d = (p[0] - temp[i][0]) ** 2 + (p[1] - temp[i][1]) ** 2
        if d < dis:
            dis = d
            min_point = temp[i]
    return min_point


def the_direction_of_the_stroke(temp1, temp2):  # 用重叠区域首尾变化的方向来判断笔画的方向
    d1 = Pretreatment.distance(temp1[0][0], temp1[0][1], temp2[0][0], temp2[0][1])
    d2 = Pretreatment.distance(temp1[0][0], temp1[0][1], temp2[len(temp2) - 1][0], temp2[len(temp2) - 1][1])
    if d1 < d2:
        return True
    else:
        return False


def Chord_weighting(temp, p):  # 弦长加权法求新的数据点
    # print("弦长加权：", temp, p)
    distance = []
    s = 0
    for i in range(1, len(temp)):
        dis = Pretreatment.distance(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1])
        s += dis
        distance.append(dis)
    x1, y1 = (p[0] - temp[len(temp) - 1][0]) / 2, (p[1] - temp[len(temp) - 1][1]) / 2
    new_temp = [temp[0]]
    l = 0
    for i in range(len(distance)):
        l += distance[i]
        w = l / s
        x, y = temp[i + 1][0] + w * x1, temp[i + 1][1] + w * y1
        new_temp.append([x, y])
    return new_temp


def overtrace_area1(temp1, temp2):
    l1 = tolerance_zone.line_length(temp1)
    l2 = tolerance_zone.line_length(temp2)
    if l1 > l2:
        a1, b1 = temp1[0], temp1[len(temp1) - 1]
    else:
        a1, b1 = temp2[0], temp2[len(temp2) - 1]
    R, T = tolerance_zone.coordinate_transformation(a1, b1)
    y1 = R @ T @ np.array([temp1[0][0], temp1[0][1], 1])
    y2 = R @ T @ np.array([temp1[len(temp1) - 1][0], temp1[len(temp1) - 1][1], 1])
    y3 = R @ T @ np.array([temp2[0][0], temp2[0][1], 1])
    y4 = R @ T @ np.array([temp2[len(temp2) - 1][0], temp2[len(temp2) - 1][1], 1])
    P1 = []
    P2 = []
    if y1[0] <= y3[0] and y3[0] <= y2[0] or y2[0] <= y3[0] and y3[0] <= y1[0]:
        P2.append(temp2[0])
        p = find_minpoint(temp2[0], temp1)
        P1.append(p)
    if y1[0] <= y4[0] and y4[0] <= y2[0] or y2[0] <= y4[0] and y4[0] <= y1[0]:
        p = find_minpoint(temp2[len(temp2) - 1], temp1)
        P2.append(temp2[len(temp2) - 1])
        P1.append(p)
    if y3[0] < y1[0] and y1[0] < y4[0] or y4[0] < y1[0] and y1[0] < y3[0]:
        p = find_minpoint(temp1[0], temp2)
        P1.append(temp1[0])
        P2.append(p)
    if y3[0] < y2[0] and y2[0] < y4[0] or y4[0] < y2[0] and y2[0] < y3[0]:
        p = find_minpoint(temp1[len(temp1) - 1], temp2)
        P1.append(temp1[len(temp1) - 1])
        P2.append(p)
    # print("p1,p2", P1, P2)
    return P1, P2


def overtrace_area2(temp1, temp2):
    point1 = []  # temp1中的点
    point2 = []  # temp2中的点
    p1 = find_minpoint(temp1[0], temp2)
    l1 = (p1[0] - temp1[0][0]) ** 2 + (p1[1] - temp1[0][1]) ** 2
    p2 = find_minpoint(temp2[0], temp1)
    l2 = (p2[0] - temp2[0][0]) ** 2 + (p2[1] - temp2[0][1]) ** 2
    if l1 < l2:
        point1.append(temp1[0])
        point2.append(p1)
    else:
        point1.append(p2)
        point2.append(temp2[0])
    p3 = find_minpoint(temp1[len(temp1) - 1], temp2)
    l3 = (p3[0] - temp1[len(temp1) - 1][0]) ** 2 + (p3[1] - temp1[len(temp1) - 1][1]) ** 2
    p4 = find_minpoint(temp2[len(temp2) - 1], temp1)
    l4 = (p4[0] - temp2[len(temp2) - 1][0]) ** 2 + (p4[1] - temp2[len(temp2) - 1][1]) ** 2
    if l3 < l4:
        point1.append(temp1[len(temp1) - 1])
        point2.append(p3)
    else:
        point1.append(p4)
        point2.append(temp2[len(temp2) - 1])
    t = point1 + point2
    return t


def modify1(temp1,temp2,overlap2):
    # s2上的重叠区域和对应的位置
    #print(len(temp1),len(temp2))
    ps_1 = overlap2[0]
    ps_n = overlap2[len(overlap2) - 1]
    s_1 = temp2.index(ps_1)
    s_n = temp2.index(ps_n)
    # s1上的重叠区域和对应的位置
    pt_1 = merge.find_minpoint(ps_1, temp1)
    pt_n = merge.find_minpoint(ps_n, temp1)
    t_1 = temp1.index(pt_1)
    t_n = temp1.index(pt_n)
    if t_1>t_n:
        overlap1=temp1[t_n:t_1+1]
        overlap2.reverse()
        ftemp=temp1[0:t_n]
        btemp=temp1[t_1:len(temp1)]
    else:
        overlap1=temp1[t_1:t_n+1]
        ftemp = temp1[0:t_1]
        btemp = temp1[t_n:len(temp1)]
    mid=[]
    for temp in overlap1:
        p=merge.find_minpoint(temp, overlap2)
        m=[(temp[0]+p[0])/2,(temp[1]+p[1])/2]
        mid.append(m)
    new_temp=ftemp+mid+btemp
    return new_temp

def extend1(temp1,temp2,overlap2):
    ftemp,btemp=standard(temp1,temp2,overlap2)
    b=ftemp[len(ftemp)-1]
    c=btemp[0]
    a=find_minpoint(c,ftemp)
    d=find_minpoint(b,btemp)
    s_a=ftemp.index(a)
    s_b = ftemp.index(b)
    s_c = btemp.index(c)
    s_d = btemp.index(d)
    new_temp=[]
    for i in range(s_a+1):
        new_temp.append(ftemp[i])
    Mtemp=btemp[s_c:s_d+1]
    Mtemp.reverse()
    ntemp=Chord_weighting(Mtemp,a)
    i=len(ntemp)-1
    while i>=0:
        new_temp.append(ntemp[i])
        i-=1
    for i in range(s_d,len(btemp)):
        new_temp.append(btemp[i])
    # print("new_temp",new_temp)
    return new_temp

def standard(temp1,temp2,overlap2):
    ps_1 = overlap2[0]
    ps_n = overlap2[len(overlap2) - 1]
    s_1 = temp2.index(ps_1)
    s_n = temp2.index(ps_n)
    # s1上的重叠区域和对应的位置
    pt_1 = merge.find_minpoint(ps_1, temp1)
    pt_n = merge.find_minpoint(ps_n, temp1)
    t_1 = temp1.index(pt_1)
    t_n = temp1.index(pt_n)
    if t_1>t_n:
        # print("变换1")
        temp2.reverse()
    elif t_1==t_n:
        if s_1==0 and t_1==0 or s_1==len(temp2)-1 and t_1==len(temp1)-1:
            # print("变换2")
            temp2.reverse()
    else:
        pass
    # d1=(temp2[0][0]-temp1[0][0])**2+(temp2[0][1]-temp1[0][1])**2
    # d2= (temp2[0][0] - temp1[2][0]) ** 2 + (temp2[0][1] - temp1[2][1]) ** 2
    # if d1>d2:
    #     ftemp=temp1
    #     btemp=temp2
    # else:
    #     print("换位置")
    #     ftemp = temp2
    #     btemp = temp1
    # max_x1,max_y1,min_x1,min_y1=Pretreatment.Outer_rect(temp1)
    # max_x2, max_y2, min_x2, min_y2 = Pretreatment.Outer_rect(temp2)
    # n=15
    # if (temp2[0][0]>=min_x1-n and temp2[0][0]<=max_x1+n) and (temp2[0][1]>=min_y1-n and temp2[0][1]<=max_y1+n):
    #     ftemp=temp1
    #     btemp=temp2
    # elif (temp1[0][0]>=min_x2-n and temp1[0][0]<=max_x2+n) and (temp1[0][1]>=min_y2-n and temp1[0][1]<=max_y2+n):
    #     print("换位置")
    #     ftemp = temp2
    #     btemp = temp1
    # else:
    #     ftemp = temp1
    #     btemp = temp2
    a = merge.find_minpoint(temp2[0], temp1)
    s_a=temp1.index(a)

    # print("a",temp1.index(a))
    if s_a in range(0,3):
        ftemp = temp2
        btemp = temp1
    else:
        ftemp = temp1
        btemp = temp2
    return ftemp,btemp


# def extend3(temp1,temp2,overlap2):
#     ps_1 = overlap2[0]
#     ps_n = overlap2[len(overlap2) - 1]
#     s_1 = temp2.index(ps_1)
#     s_n = temp2.index(ps_n)
#     # s1上的重叠区域和对应的位置
#     pt_1 = merge.find_minpoint(ps_1, temp1)
#     pt_n = merge.find_minpoint(ps_n, temp1)
#     t_1 = temp1.index(pt_1)
#     t_n = temp1.index(pt_n)
#     if t_1 > t_n:
#         print("方向相反")
#         temp2.reverse()
#     elif t_1 == t_n:
#         if not (s_1==0 and t_n==len(temp1)-1 or s_n==0 and t_1==len(temp1)-1):
#             print("方向相反1")
#             temp2.reverse()
#     else:
#         pass







