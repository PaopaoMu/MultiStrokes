import numpy as np
import merge
import tolerance_zone
import math
import break_point
import Pretreatment
import break_point
import tolerance_zone


def angle(temp1, temp2):  # 两个笔画首尾的夹角是否小于60
    breakpoint1 = break_point.turning_point(temp1)
    breakpoint2 = break_point.turning_point(temp2)
    t1 = [breakpoint1[len(breakpoint1) - 1][0] - breakpoint1[len(breakpoint1) - 2][0],
          breakpoint1[len(breakpoint1) - 1][1] - breakpoint1[len(breakpoint1) - 2][1]]
    t2 = [breakpoint2[1][0] - breakpoint2[0][0],
          breakpoint2[1][1] - breakpoint2[0][1]]
    theta = (t1[0] * t2[0] + t1[1] * t2[1]) / ((
                                                       (t1[0] * t1[0] + t1[1] * t1[1]) ** 0.5) * (
                                                       (t2[0] * t2[0] + t2[1] * t2[1]) ** 0.5))
    a = math.acos(theta)
    # print("角度",a)
    if a <= math.pi / 3:
        print("首尾笔画小于60度")
        return True
    else:
        print("首尾笔画大于60度")
        return False


def extend_stroke(temp1, temp2):
    l = tolerance_zone.the_lengthest(temp1)
    y = 3 / 4 * float('%.2f' % (l ** 0.5)) + 2  # 找到容差宽度
    max_corpoint = break_point.turning_point(temp1)  # 折线化的点
    max_corpoint.append(temp2[int(len(temp2) / 2)])
    max_corpoint.append(temp2[len(temp2) - 1])
    temp = []
    for i in range(1, len(max_corpoint)):
        f_point = max_corpoint[i - 1]
        b_point = max_corpoint[i]
        # print(f_point,b_point)
        R, T = tolerance_zone.coordinate_transformation(f_point, b_point)
        length = Pretreatment.distance(f_point[0], f_point[1], b_point[0], b_point[1])
        x = length / 2  # 容差长度范围
        h = 0
        while h < len(temp2):
            X = np.array([temp2[h][0], temp2[h][1], 1])
            Y = R @ T @ X
            r1 = ((temp2[h][0] - f_point[0]) ** 2 + (temp2[h][1] - f_point[1]) ** 2)
            r2 = ((temp2[h][0] - b_point[0]) ** 2 + (temp2[h][1] - b_point[1]) ** 2)
            if math.fabs(Y[0]) <= x and math.fabs(Y[1]) <= y or r1 <= y * y or r2 <= y * y:
                if temp2[h] in temp:
                    pass
                else:
                    a = temp2[h]
                    temp.append(a)
            h += 1
    k = len(temp) / len(temp2)
    print("延伸笔画的比率", k)
    return k


def angle_bisector(temp1, temp2):  # 判断是否延伸笔画
    overtrace = merge.overtrace_area(temp1, temp2)
    a = overtrace[0]
    b = overtrace[1]
    c = overtrace[2]
    d = overtrace[3]
    if a == b and c == d:
        m1 = a
        m2 = c
    else:
        m1 = [(a[0] + c[0]) / 2, (a[1] + c[1]) / 2]
        m2 = [(b[0] + d[0]) / 2, (b[1] + d[1]) / 2]
    R, T = tolerance_zone.coordinate_transformation(m1, m2)
    a = temp1.index(overtrace[0])
    b = temp1.index(overtrace[1])
    c = temp2.index(overtrace[2])
    d = temp2.index(overtrace[3])
    # print("a,b,c,d", a, b, c, d)
    m1 = int((a + b) / 2)
    m2 = int((c + d) / 2)
    if len(temp1) - m1 < m1 - 0:
        h = temp1[0]
    else:
        h = temp1[len(temp1) - 1]
    if len(temp2) - m2 < m2 - 0:
        l = temp2[0]
    else:
        l = temp2[len(temp2) - 1]
    h1 = np.array([h[0], h[1], 1])
    l1 = np.array([l[0], l[1], 1])
    new_h = R @ T @ h1
    new_l = R @ T @ l1
    # print(new_h, new_l)
    if new_h[0] * new_l[0] < 0:
        print("笔画位于y轴两侧")
        return True
    else:
        print("笔画位于y轴同侧")
        return False


def is_extend(temp1, temp2):
    d1 = Pretreatment.distance(temp1[0][0], temp1[0][1], temp2[0][0], temp2[0][1])
    d2 = Pretreatment.distance(temp1[0][0], temp1[0][1], temp2[1][0], temp2[1][1])
    if d1 < d2:
        ftemp = temp1
        btemp = temp2
    else:
        ftemp = temp2
        btemp = temp1
    if angle(ftemp, btemp) and angle_bisector(ftemp, btemp) and extend_stroke(ftemp, btemp) > 0.8:
        # if  angle_bisector(ftemp, btemp) :
        return True
    else:
        return False


def is_branch(temp1, temp2, mtemp):
    point2 = mtemp[len(mtemp) - 1]
    point1 = merge.find_minpoint(point2, temp1)
    T1 = temp1[temp1.index(point1):len(temp1)]
    T2 = temp2[temp2.index(point2):len(temp2)]
    b1 = tolerance_zone.line_length(T1)
    b2 = tolerance_zone.line_length(T2)
    point22 = mtemp[0]
    point11 = merge.find_minpoint(point22, temp1)
    T11 = temp1[0:temp1.index(point11) + 1]
    T22 = temp2[0:temp2.index(point22) + 1]
    b11 = tolerance_zone.line_length(T11)
    b22 = tolerance_zone.line_length(T22)
    mtemp2=temp1[temp1.index(point11):temp1.index(point1)+1]
    if b1 == 0 and b2 == 0 or b11 == 0 and b22 == 0:
        return False
    if b1 == 0 or b2 == 0:
        if b11 < b22:
            k2 = b11 / b22
        else:
            k2 = b22 / b11
        if k2 < 0.1:
            if len(mtemp) < 2 or len(mtemp2) < 2:
                if stroke_orient(temp1, temp2) < math.pi / 2:
                    return True
                else:
                    return False
            if stroke_orient(mtemp2, mtemp)<=math.pi/3:
                return True
            else:
                return False
        else:
            return False
    else:
        if b1 < b2:
            k1 = b1 / b2
        else:
            k1 = b2 / b1
        if k1 < 0.1:
            if len(mtemp) < 2 or len(mtemp2) < 2:
                if stroke_orient(temp1, temp2) < math.pi / 2:
                    return True
                else:
                    return False
            if stroke_orient(mtemp2, mtemp)<=math.pi/3:
                return True
            else:
                return False
        else:
            return False


def stroke_orient(s1, s2):
    print("s1,s2",s1,s2)
    if s1==[]or s2==[]:
        return False
    m1 = [s1[len(s1) - 1][0] - s1[0][0], s1[len(s1) - 1][1] - s1[0][1]]
    m2 = [s2[len(s2) - 1][0] - s2[0][0], s2[len(s2) - 1][1] - s2[0][1]]
    theta = (m1[0] * m2[0] + m1[1] * m2[1]) / (
            ((m1[0] * m1[0] + m1[1] * m1[1]) ** 0.5) * ((m2[0] * m2[0] + m2[1] * m2[1]) ** 0.5))
    a = math.acos(theta)
    return a


def extend_strokes(s1,s2,overlap):
    #s2上的重叠区域和对应的位置
    ps_1=overlap[0]
    ps_n=overlap[len(overlap)-1]
    s_1=s2.index(ps_1)
    s_n=s2.index(ps_n)
    # s1上的重叠区域和对应的位置
    pt_1=merge.find_minpoint(ps_1,s1)
    pt_n=merge.find_minpoint(ps_n,s1)
    t_1=s1.index(pt_1)
    t_n=s1.index(pt_n)
    if (s_1 in range(3,len(s2)-3) and s_n in range(3,len(s2)-3)) or (t_1 in range(3,len(s1)-3) and t_n in range(3,len(s1)-3)):
        return False










def orient(p1,p2):
    x1=p2[0]-p1[0]
    y1=p2[1]-p1[1]
    if x1>0 or y1>0:
        num=1
    else:
        num=0
    return num



