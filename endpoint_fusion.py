import numpy as np


def Endpoint(ALL):  # 对笔画进行分类
    m = len(ALL)
    A = np.zeros((m, m))
    for i in range(m):
        s1 = ALL[i]
        for j in range(i + 1, m):
            s2 = ALL[j]
            num = mask(s1, s2)
            h=i-1
            A[i][j] =num
            #
    print("A", A)

    return A


def mask(s1, s2):
    p11 = s1[0]
    p12 = s1[len(s1) - 1]
    p21 = s2[0]
    p22 = s2[len(s2) - 1]
    d1 = (p11[0] - p21[0]) ** 2 + (p11[1] - p21[1]) ** 2
    d2 = (p11[0] - p22[0]) ** 2 + (p11[1] - p22[1]) ** 2
    d3 = (p12[0] - p21[0]) ** 2 + (p12[1] - p21[1]) ** 2
    d4 = (p12[0] - p22[0]) ** 2 + (p12[1] - p22[1]) ** 2
    w =900
    if d1 < w:  # 1代表首首相连、2代表首尾、3代表尾首、4代表尾尾
        num = 1
    elif d2 < w:
        num = 2
    elif d3 < w:
        num = 3
    elif d4 < w:
        num = 4
    else:
        num = 0
    return num


def end_fusion(all_stroke):
    print("连接前的",all_stroke)
    Endpoint=[]#图中所有待融合端点
    for temp in all_stroke:
        p0=temp[0]
        p1=temp[len(temp)-1]
        end=[p0,p1]
        Endpoint.append(end)
    endnote=[]#能够聚在一起的节点聚点
    node_location=[]#记录节点所在位置
    h=0
    while h<len(Endpoint):
        note=[]
        location=[]
        if Endpoint[h][0]!=0:
            note.append(Endpoint[h][0])
            location.append([h,0])
            Endpoint[h][0] = 0
        elif Endpoint[h][1]!=0:
            note.append(Endpoint[h][1])
            location.append([h,1])
            Endpoint[h][1] = 0
        else:
            h+=1
            continue
        k=h+1
        while k<len(Endpoint):
            if Endpoint[k][0] != 0:
                distance=(note[0][0] - Endpoint[k][0][0]) ** 2 + (note[0][1] - Endpoint[k][0][1]) ** 2
                if distance<100:
                    note.append(Endpoint[k][0])
                    location.append([k, 0])
                    Endpoint[k][0] = 0
            if Endpoint[k][1] != 0:
                distance=(note[0][0] - Endpoint[k][1][0]) ** 2 + (note[0][1] - Endpoint[k][1][1]) ** 2
                if distance<100:
                    note.append(Endpoint[k][1])
                    location.append([k, 1])
                    Endpoint[k][1] = 0
            k+=1
        m=[0,0]
        for temp in note:
            m[0]=m[0]+temp[0]
            m[1]=m[1]+temp[1]
        m=[m[0]/len(note),m[1]/len(note)]
        endnote.append(m)
        node_location.append(location)
    astroke = []
    for temp in all_stroke:
        stroke=[]
        for i in temp:
            stroke.append(i)
        astroke.append(stroke)
    new_all=list(np.arange(len(all_stroke)))
    for i in range(len(endnote)):
        cnode=endnote[i]
        clocation=node_location[i]
        for j in range(len(clocation)):
            site=clocation[j]
            num=site[0]#哪一条笔画
            loc=site[1]#首还是尾
            # stroke=[]
            # a_str=all_stroke[num]
            # for temp in a_str:
            #     stroke.append(temp)
            stroke1=astroke[num]
            if loc==0:
                stroke1[0]=cnode
            if loc==1:
                stroke1[len(stroke1)-1]=cnode
            new_all[num]=stroke1
    print("连接后的",new_all)
    return new_all











