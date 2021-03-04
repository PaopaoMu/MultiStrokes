import numpy as np
import Pretreatment
import math
import break_point



# hermit插值法拟合
def Graceful_curve(temp):
    Bpoint = resample_point(temp)
    Bpoint.insert(0,Bpoint[0])
    Bpoint.append(Bpoint[len(Bpoint)-1])
    Bpoint.insert(0, Bpoint[0])
    Bpoint.append(Bpoint[len(Bpoint) - 1])
    i=0
    Temp = []
    while i<len(Bpoint)-3:
        new_temp=B_spline_curve(Bpoint[i],Bpoint[i+1],Bpoint[i+2],Bpoint[i+3])
        for n in new_temp:
            Temp.append(n)
        i+=1
    # print("拟合后",Temp)
    return Temp


def hermite_interpolation(p1, p2, dp1, dp2, temp):  # hermite插值曲线
    P = []
    # P.append(temp[0])
    u = 0
    while u <= 1:
        h0 = 2 * u * u * u - 3 * u * u + 1
        h1 = -2 * u * u * u + 3 * u * u
        h2 = u * u * u - 2 * u * u + u
        h3 = u * u * u - u * u
        x = p1[0] * h0 + p2[0] * h1 + dp1[0] * h2 + dp2[0] * h3
        y = p1[1] * h0 + p2[1] * h1 + dp1[1] * h2 + dp2[1] * h3
        P.append([x, y])
        u = 0.1 + u
    return P


def Akima(p1, p2, p3, p4, p5):  # 求p3斜率
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    p4 = np.array(p4)
    p5 = np.array(p5)
    l1 = p2 - p1
    l2 = p3 - p2
    l3 = p4 - p3
    l4 = p5 - p4
    a = np.linalg.norm(l4 - l3) * l2 + np.linalg.norm(l2 - l1) * l3
    b = np.linalg.norm(l4 - l3) + l2 + np.linalg.norm(l2 - l1)
    t = a / b
    # print("切线方向", t)
    return t


def Three_point_chord_weighting(p1, p2, p3):  # 求p2斜率
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    v1 = p2 - p1
    v2 = p3 - p2
    l1 = Pretreatment.distance(p1[0], p1[1], p2[0], p2[1])
    l2 = Pretreatment.distance(p2[0], p2[1], p3[0], p3[1])
    nv1 = np.linalg.norm(v1)
    nv2 = np.linalg.norm(v2)
    t = (l1 / l2) * (v2 / nv2) + (l2 / l1) * (v2 / nv2)
    # print("切线方向", t)
    return t


def cardinal(p1, p2, p3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    t = (p3 - p1) / 2.0
    # print("切线方向",t)
    return t


def resample_point(temp):
    new_temp = []
    for i in range(len(temp)):
        if i % 20 == 0:
            new_temp.append(temp[i])
        if i == len(temp) - 1 and i % 10 != 0:
            new_temp.append(temp[i])
    return new_temp


def B_spline_curve(p0,p1,p2,p3):  # B样条拟合曲线
    P = []
    u = 0
    while u <= 1:
        B03 = ((1 - u) ** 3) / 6
        B13 = (3 * u ** 3 - 6 * u ** 2 + 4) / 6
        B23 = (-3 * u ** 3 + 3 * u ** 2 + 3 * u + 1) / 6
        B33 = u**3/6
        x =B03*p0[0]+B13*p1[0]+B23*p2[0]+B33*p3[0]
        y =B03*p0[1]+B13*p1[1]+B23*p2[1]+B33*p3[1]
        P.append([x, y])
        u = 0.05 + u
    return P
