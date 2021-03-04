from tkinter import *
import tolerance_zone
import merge
import Fit_curve
import json
import random
import break_point
import is_extend_stroke
import endpoint_fusion
import numpy as np
import tkinter as tk
import Pretreatment
import datetime
import time

root = Tk()
root.title("draw picture")
root.configure(background="light blue")
menubar=Menu(root, bg="#20232A")
fmenu1=Menu(root)
fmenu2=Menu(root)
w1 = Canvas(root, width=500, height=500, background="white")
w1.pack(side=LEFT)
w3 = Canvas(root, width=500, height=500, background="white")
w3.pack(side=RIGHT)

# w2 = Canvas(root, width=500, height=500, background="white")
# w2.pack(side=RIGHT)
N = 1

point = []#每一笔的笔画数据点
point_gather = []#全部的数据点
pre_point_gather=[]#预处理以后的
sim_stroke=[]



def paint1(event):  # 可以知道笔画的坐标
    x = event.x
    y = event.y
    a = [x, y]
    point.append(a)
    length = len(point)
    w1.create_oval(x - 1, y -1, x + 1, y + 1, outline="red", fill="red")
    if length != (0, 1):
        w1.create_line(point[length - 1][0], point[length - 1][1], point[length - 2][0], point[length - 2][1],
                       fill="red", width=2)


def reset(event):  # 存笔画
    temp = []
    for i in point:
        temp.append(i)
    point_gather.append(temp)
    point.clear()
    fileObject = open('在线手绘.txt', 'w')
    for ip in point_gather:
        fileObject.write(str(ip))
        fileObject.write('\n')
    fileObject.close()


def flower():
    global point_gather
    f = open('鲜花.txt', 'r')
    temp1 = []
    for line in f:
        list_line = json.loads(line)
        temp1.append(list_line)
    f.close()
    print("笔画", len(temp1))
    point_gather = temp1
    for temp in point_gather:
        num = len(temp)
        for i in range(num):
            w1.create_oval(temp[i][0] - (N - 2), temp[i][1] - (N - 2), temp[i][0] + (N - 2), temp[i][1] + (N - 2),
                           outline="black", fill="black")
            if i != 0:
                w1.create_line(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1], fill="black", width=2)


def eagle():
    global point_gather
    f = open('老鹰.txt', 'r')
    temp1 = []
    for line in f:
        list_line = json.loads(line)
        temp1.append(list_line)
    f.close()
    print("笔画", len(temp1))
    point_gather = temp1
    for temp in point_gather:
        num = len(temp)
        for i in range(num):
            w1.create_oval(temp[i][0] - (N - 2), temp[i][1] - (N - 2), temp[i][0] + (N - 2), temp[i][1] + (N - 2),
                           outline="black", fill="black")
            if i != 0:
                w1.create_line(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1], fill="black", width=2)


def girl():
    global point_gather
    f = open('女孩1.txt', 'r')
    temp1 = []
    for line in f:
        list_line = json.loads(line)
        temp1.append(list_line)
    f.close()
    print("女孩笔画",len(temp1))
    point_gather = temp1
    for temp in point_gather:
        num = len(temp)
        for i in range(num):
            w1.create_oval(temp[i][0] - (N - 2), temp[i][1] - (N - 2), temp[i][0] + (N - 2), temp[i][1] + (N - 2),
                           outline="black", fill="black")
            if i != 0:
                w1.create_line(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1], fill="black", width=2)


def building():
    global point_gather
    f = open('海豚1.txt', 'r')
    temp1 = []
    for line in f:
        list_line = json.loads(line)
        temp1.append(list_line)
    f.close()
    print("笔画", len(temp1))
    point_gather = temp1
    for temp in point_gather:
        num = len(temp)
        for i in range(num):
            w1.create_oval(temp[i][0] - (N - 2), temp[i][1] - (N - 2), temp[i][0] + (N - 2), temp[i][1] + (N - 2),
                           outline="black", fill="black")
            if i != 0:
                w1.create_line(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1], fill="black", width=2)


def pre_processing(point):  # 预处理
    new_point_gather = []
    point_gather1 =Pretreatment.deletion(point)  # 去除多余的点
    for temp in point_gather1:
        temp3 = Pretreatment.renew_process(temp)  # 重采样
        temp4 = Pretreatment.smooth(temp3)  # 平滑
        new_point_gather.append(temp4)
    return new_point_gather


def pre():
    global point_gather
    global pre_point_gather
    pre_point_gather = pre_processing(point_gather)
    for temp in pre_point_gather:
        num = len(temp)
        # for i in range(num):
        #     w2.create_oval(temp[i][0] - (N - 2), temp[i][1] - (N - 2), temp[i][0] + (N - 2), temp[i][1] + (N - 2),
        #                    outline="black", fill="black")
        #     if i != 0:
        #         w2.create_line(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1], fill="black", width=2)


def first_simplify():  #简化
    w3.delete(tk.ALL)
    start = time.time()
    global pre_point_gather
    print(pre_point_gather)
    B = []
    B.append(pre_point_gather[0])
    p = list(np.arange(len(pre_point_gather)))
    for i in range(1, len(pre_point_gather)):
        temp1 = B[len(B) - 1]
        temp2 = pre_point_gather[i]
        l1=tolerance_zone.line_length(temp1)
        l2=tolerance_zone.line_length(temp2)
        if l1>l2:
            max_temp=temp1
            min_temp=temp2
        else:
            max_temp=temp2
            min_temp=temp1
        p_point,judge = tolerance_zone.is_overdraw(max_temp, min_temp)
        if judge > 0:
            if judge ==1:  # 考虑修改类融合
                # print("修改类")
                del B[len(B) - 1]
                # new_temp = merge.modify(max_temp, min_temp)
                new_temp = merge.modify1(max_temp, min_temp, p_point)
                B.append(new_temp)
                p[i]=p[i-1]
            else:  # 延伸类融合
                # if is_extend_stroke.is_branch(max_temp,min_temp,p_point):
                # if is_extend_stroke.is_extend(temp1, temp2):
                # print(max_temp,min_temp)
                if is_extend_stroke.extend_strokes(max_temp, min_temp, p_point):
                    # print(max_temp, min_temp)
                    # print("延伸类")
                    del B[len(B) - 1]
                    new_temp = merge.extend1(max_temp, min_temp, p_point)
                    # new_temp = merge.extend(temp1,temp2)
                    B.append(new_temp)
                    p[i] = p[i - 1]
                else:
                    # print("无关笔画2")
                    B.append(temp2)
        else:
            # print("无关笔画3")
            B.append(temp2)
    global sim_stroke
    sim_stroke=B
    # A = endpoint_fusion.end_fusion(B)
    # color_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    # p.insert(0,0)
    # color = ''
    # for i in range(6):
    #     color_number = color_list[random.randint(0, 15)]
    #     color += color_number
    # for i in range(len(pre_point_gather)):
    #     temp=pre_point_gather[i]
    #     if p[i]!=p[i+1]:
    #         color = ''
    #         for i in range(6):
    #             color_number = color_list[random.randint(0, 15)]
    #             color += color_number
    #     for j in range(len(temp)):
    #         w2.create_oval(temp[j][0] - (N - 2), temp[j][1] - (N - 2), temp[j][0] + (N - 2), temp[j][1] + (N - 2),
    #                        outline='#' + color, fill='#' + color)
    #         if j != 0:
    #             w2.create_line(temp[j - 1][0], temp[j - 1][1], temp[j][0], temp[j][1], fill='#' + color, width=N)
    # for i in range(len(pre_point_gather)):
    #     # b_point1=break_point.turning_point(pre_point_gather[i])
    #     b_point2=break_point.turning_point1(pre_point_gather[i])
    #     # for j in range(len(b_point1)):
    #     #     w1.create_oval(b_point1[j][0] -3, b_point1[j][1] - 3,b_point1[j][0] +3, b_point1[j][1] +3,
    #     #                    outline="red", fill="red")
    #     for j in range(len(b_point2)):
    #         w1.create_oval(b_point2[j][0] - 2, b_point2[j][1] - 2,b_point2[j][0] + 2, b_point2[j][1] + 2,
    #                        outline="red", fill="red")
    print("简化后笔画", len(B))
    for temp1 in B:
        temp=Fit_curve.Graceful_curve(temp1)
        num = len(temp)
        for i in range(num):
            w3.create_oval(temp[i][0] - 0.5, temp[i][1] - 0.5, temp[i][0] +0.5, temp[i][1] + 0.5,
                           outline="blue", fill="blue")
            # w1.create_oval(temp[i][0] - 0.5, temp[i][1] - 0.5, temp[i][0] + 0.5, temp[i][1] + 0.5,
            #                outline="blue", fill="blue")
            if i != 0:
                w3.create_line(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1], fill="blue", width=1)
                # w1.create_line(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1], fill="blue", width=1)
    end = time.time()
    print("循环运行时间:%.2f秒" % (end - start))
    print(sim_stroke)


def second_simplify():  #简化
    w3.delete(tk.ALL)
    start = time.time()
    global sim_stroke
    A=[]
    i=0
    B=[]
    for temp in sim_stroke:
        B.append(temp)
    while B:
        A.append(B[0])
        del B[0]
        i=0
        m=len(B)
        while i<m:
            temp1=A[len(A)-1]
            temp2=B[i]
            l1 = tolerance_zone.line_length(temp1)
            l2 = tolerance_zone.line_length(temp2)
            if l1 > l2:
                max_temp = temp1
                min_temp = temp2
            else:
                max_temp = temp2
                min_temp = temp1
            p_point, judge = tolerance_zone.is_overdraw(max_temp, min_temp)
            print(judge)
            if judge > 0:
                if judge > 0.8:  # 考虑修改类融合
                    print("修改类")
                    del A[len(A) - 1]
                    new_temp = merge.modify1(max_temp, min_temp, p_point)
                    A.append(new_temp)
                    del B[i]
                    m=len(B)
                else:  # 延伸类融合
                    if is_extend_stroke.extend_strokes(max_temp, min_temp, p_point):
                        print("延伸类")
                        del A[len(A) - 1]
                        new_temp = merge.extend1(max_temp, min_temp, p_point)
                        A.append(new_temp)
                        del B[i]
                        m = len(B)
                    else:
                        print("无关1")
                        i+=1
            else:
                print("无关2")
                i+=1

    print("简化后笔画", len(A),A)
    for temp1 in A:
        temp=Fit_curve.Graceful_curve(temp1)
        num = len(temp)
        for i in range(num):
            w3.create_oval(temp[i][0] - 0.5, temp[i][1] - 0.5, temp[i][0] +0.5, temp[i][1] + 0.5,
                           outline="blue", fill="blue")
            # w1.create_oval(temp[i][0] - 0.5, temp[i][1] - 0.5, temp[i][0] + 0.5, temp[i][1] + 0.5,
            #                outline="blue", fill="blue")
            if i != 0:
                w3.create_line(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1], fill="blue", width=1)
                # w1.create_line(temp[i - 1][0], temp[i - 1][1], temp[i][0], temp[i][1], fill="blue", width=1)
    end = time.time()
    print("循环运行时间:%.2f秒" % (end - start))




# B1 = Button(root, text="鲜花", font=("幼圆", 15), fg="black", bg="white", command=flower)
# B1.pack(side=TOP, padx=30, pady=20)
# B2 = Button(root, text="老鹰", font=("幼圆", 15), fg="black", bg="white", command=eagle)
# B2.pack(side=TOP, padx=30, pady=20)
# B3 = Button(root, text="女孩", font=("幼圆", 15), fg="black", bg="white", command=girl)
# B3.pack(side=TOP, padx=30, pady=20)
# B4 = Button(root, text="建筑", font=("幼圆", 15), fg="black", bg="white", command=building)
# B4.pack(side=TOP, padx=30, pady=20)
# B5 = Button(root, text="预处理", font=("幼圆", 15), fg="black", bg="white", command=pre)
# B5.pack(side=TOP, padx=30, pady=20)
# B6 = Button(root, text="简化", font=("幼圆", 15), fg="black", bg="white", command=first_simplify)
# B6.pack(side=TOP, padx=30, pady=20)
# B7 = Button(root, text="第二次简化", font=("幼圆", 15), fg="black", bg="white", command=second_simplify)
# B7.pack(side=TOP, padx=30, pady=20)
menubar.add_cascade(label="文件",menu=fmenu1)
fmenu1.add_command(label="鲜花",command=flower)
fmenu1.add_command(label="老鹰",command=eagle)
fmenu1.add_command(label="女孩",command=girl)
fmenu1.add_command(label="建筑",command=building)
menubar.add_cascade(label="选项",menu=fmenu2)
fmenu2.add_command(label="预处理",command=pre)
fmenu2.add_command(label="第一次简化",command=first_simplify)
fmenu2.add_command(label="第二次简化",command=second_simplify)

root.config(menu=menubar)

w1.bind("<B1-Motion>", paint1)  # 将画布与鼠标按下与滑动绑定在一起
w1.bind("<ButtonRelease>", reset)  # 将鼠标释放与数组清空绑定在一起

mainloop()
