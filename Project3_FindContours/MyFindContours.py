import math

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from statistics import mean
from math import sqrt

img = mpimg.imread('triangle.png')


def RGB2GRAY(image):
    w, h = image.shape[:2]
    # new Image dimension with 4 attribute in each pixel
    newImage = np.zeros([w, h, 4])
    # ratio of RGB will be between 0 and 1
    for i in range(w):
        for j in range(h):
            lst = [float(img[i][j][0]), float(img[i][j][1]), float(img[i][j][2])]
            avg = float(mean(lst))
            newImage[i][j][0] = avg
            newImage[i][j][1] = avg
            newImage[i][j][2] = avg
            newImage[i][j][3] = 1  # alpha value to be 1
    return newImage


def threshold(image, thresh_value):
    thresh_value = thresh_value / 255
    w, h = image.shape[:2]
    newImage = np.zeros([w, h, 4])
    for i in range(w):
        for j in range(h):
            if image[i][j][0] < thresh_value:
                newImage[i][j][0] = 0
            else:
                newImage[i][j][0] = 1
            if image[i][j][1] < thresh_value:
                newImage[i][j][1] = 0
            else:
                newImage[i][j][1] = 1
            if image[i][j][2] < thresh_value:
                newImage[i][j][2] = 0
            else:
                newImage[i][j][2] = 1

            newImage[i][j][3] = 1
    return newImage


def edgeDetection(image):
    w, h = image.shape[:2]
    newImage = np.zeros([w, h, 4])
    r_prev, g_prev, b_prev = 0, 0, 0
    for i in range(w):
        for j in range(h):

            if image[i][j][0] == 1 and r_prev == 0:
                newImage[i][j][0] = 1
                newImage[i][j][1] = 1
                newImage[i][j][2] = 1
            if image[i][j][0] == 0 and r_prev == 1:
                newImage[i][j][0] = 1
                newImage[i][j][1] = 1
                newImage[i][j][2] = 1
            if image[i - 1][j][0]:
                if image[i - 1][j][0] == 1 and image[i][j][0] == 0:
                    newImage[i][j][0] = 1
                    newImage[i][j][1] = 1
                    newImage[i][j][2] = 1
            if i + 1 < w:
                if image[i + 1][j][0] == 1 and image[i][j][0] == 0:
                    newImage[i][j][0] = 1
                    newImage[i][j][1] = 1
                    newImage[i][j][2] = 1
            r_prev = image[i][j][0]
            newImage[i][j][3] = 1
    return newImage


coordinatesX = []
coordinatesY = []


def getCoordinatesX(image):
    coordinatesX.clear()
    w, h = image.shape[:2]
    for i in range(w):
        for j in range(h):
            if image[i][j][0] == 1:
                coordinatesX.append([i, j])
    return coordinatesX


def getCoordinatesY(image):
    coordinatesY.clear()
    w, h = image.shape[:2]
    for j in range(h - 1, 0, -1):
        for i in range(w):
            if image[i][j][0] == 1:
                coordinatesY.append([i, j])
    return coordinatesY


def distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def PerpendicularDistance(point, start, end):
    if start == end:
        return distance(point, start)
    else:
        n = abs(
            (end[0] - start[0]) * (start[1] - point[1]) -
            (start[0] - point[0]) * (end[1] - start[1])
        )
        d = sqrt(
            (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
        )
        return n / d


def RDP(pointList1, pointList2, epsilon):
    dmax1 = 0.0
    dmax2 = 0.0
    index1 = 0
    index2 = 0
    for i in range(1, len(pointList1) - 1):
        d1 = PerpendicularDistance(pointList1[i], pointList1[0], pointList1[-1])
        if d1 > dmax1:
            index1 = i
            dmax1 = d1
    for j in range(1, len(pointList2) - 1):
        d2 = PerpendicularDistance(pointList2[j], pointList2[0], pointList2[-1])
        if d2 > dmax2:
            index2 = j
            dmax2 = d2

    if dmax1 >= epsilon and dmax2 >= epsilon:
        resultList1 = RDP(pointList1[:index1 + 1], pointList2[:index2 + 1], epsilon)[:-1] + RDP(pointList1[index1:],
                                                                                                pointList2[index2:],
                                                                                                epsilon)
    else:
        resultList1 = [pointList1[0], pointList1[-1], pointList2[0], pointList2[-1]]
    list2 = []
    if resultList1:
        for item in resultList1:
            if item not in list2:
                list2.append(item)
    else:
        return resultList1
    return list2


def RDP_Result(coordinates, image, min_arc_length):
    w, h = image.shape[:2]
    a = 0
    # new Image dimension with 4 attribute in each pixel
    newImage = np.zeros([w, h, 4], np.uint8)
    # ratio of RGB will be between 0 and 1
    for i in range(w):
        for j in range(h):
            newImage[i][j][2] = 0
            newImage[i][j][3] = 0
            newImage[i][j][2] = 0
            newImage[i][j][3] = 255
    for c in range(len(coordinates)):
        a += 1
        newImage[coordinates[c][0]][coordinates[c][1]][0] = 0
        newImage[coordinates[c][0]][coordinates[c][1]][1] = 0
        newImage[coordinates[c][0]][coordinates[c][1]][2] = 255
        newImage[coordinates[c][0]][coordinates[c][1]][3] = 255
    newImage[coordinatesX[0][0]][coordinatesX[0][1]][0] = 0
    newImage[coordinatesX[0][0]][coordinatesX[0][1]][1] = 255
    newImage[coordinatesX[0][0]][coordinatesX[0][1]][2] = 0
    newImage[coordinatesX[0][0]][coordinatesX[0][1]][3] = 255

    newImage[coordinatesX[-1][0]][coordinatesX[-1][1]][0] = 0
    newImage[coordinatesX[-1][0]][coordinatesX[-1][1]][1] = 255
    newImage[coordinatesX[-1][0]][coordinatesX[-1][1]][2] = 0
    newImage[coordinatesX[-1][0]][coordinatesX[-1][1]][3] = 255

    newImage[coordinatesY[0][0]][coordinatesY[0][1]][0] = 255
    newImage[coordinatesY[0][0]][coordinatesY[0][1]][1] = 0
    newImage[coordinatesY[0][0]][coordinatesY[0][1]][2] = 0
    newImage[coordinatesY[0][0]][coordinatesY[0][1]][3] = 255

    newImage[coordinatesY[-1][0]][coordinatesY[-1][1]][0] = 255
    newImage[coordinatesY[-1][0]][coordinatesY[-1][1]][1] = 0
    newImage[coordinatesY[-1][0]][coordinatesY[-1][1]][2] = 0
    newImage[coordinatesY[-1][0]][coordinatesY[-1][1]][3] = 255
    print(a)
    # print(len(coordinates))
    return newImage


def angle(list):
    ang = [[], []]
    for i in range(len(list)):
        if i - 1 >= 0 and i + 1 < len(list):
            # a^2=c^2+b^2-2bc cos(Q)
            # print(list[i + 1], list[i], list[i - 1], "n")
            if list[i + 1] != list[i - 1] and list[i - 1] != list[i] and list[i + 1] != list[i]:
                a = math.pow(
                    (abs(list[i + 1][0] - list[i - 1][0]) ^ 2
                     + abs(list[i + 1][1] - list[i - 1][1]) ^ 2)
                    , 0.5)
                b = math.pow(
                    (abs(list[i][0] - list[i - 1][0]) ^ 2
                     + abs(list[i][1] - list[i - 1][1]) ^ 2)
                    , 0.5)
                c = math.pow(
                    (abs(list[i + 1][0] - list[i][0]) ^ 2
                     + abs(list[i + 1][1] - list[i][1]) ^ 2)
                    , 0.5)
                # Q=arccos(a^2-b^2-c^2/-2bc)
                if c == 0:
                    c = 0.1
                if b == 0:
                    b = 0.1
                val = round((round(a, 8) ** 2 - round(b, 8) ** 2 - round(c, 8) ** 2) / (-2 * round(b, 8) * round(c, 8)),
                            8)
                # print(val)
                if val < -1:
                    # print(round(val-math.trunc(val),8))
                    val = round(val - math.trunc(val), 8)
                else:
                    val = (math.acos(val) * 180) / math.pi
                if val < 0:
                    val = 180 + val
                print("point1: ", a," point2: ", b," point3: ", c," angle :",val)
                ang[1].append(val)
                ang[0].append([list[i - 1], list[i], list[i + 1]])
    # print(list[-2], list[-1], list[0], "n1")
    b = pow(
        (abs(list[-2][0] - list[-1][0]) ^ 2
         + abs(list[-2][1] - list[-1][1]) ^ 2)
        , 0.5)
    c = pow(
        (abs(list[-1][0] - list[0][0]) ^ 2
         + abs(list[-1][1] - list[0][1]) ^ 2)
        , 0.5)
    a = pow(
        (abs(list[0][0] - list[-2][0]) ^ 2
         + abs(list[0][1] - list[-2][1]) ^ 2)
        , 0.5)
    if c == 0:
        c = 0.1
    if b == 0:
        b = 0.1
    val = round((round(a, 8) ** 2 - round(b, 8) ** 2 - round(c, 8) ** 2) / (-2 * round(b, 8) * round(c, 8)), 8)
    # print(val)
    if val < -1:
        # print(round(val-math.trunc(val),8))
        val = round(val - math.trunc(val), 8)
    else:
        val = (math.acos(val) * 180) / math.pi
    if val < 0:
        val = 180 + val
    print("point1: ", a," point2: ", b," point3: ", c," angle :",val)
    ang[1].append(val)
    ang[0].append([list[0], list[-1], list[-2]])
    # print(list[-1], list[0], list[1], "n2")
    b = pow(
        (abs(list[-1][0] - list[0][0]) ^ 2
         + abs(list[-1][1] - list[0][1]) ^ 2)
        , 0.5)
    c = pow(
        (abs(list[0][0] - list[1][0]) ^ 2
         + abs(list[0][1] - list[1][1]) ^ 2)
        , 0.5)
    a = pow(
        (abs(list[1][0] - list[-1][0]) ^ 2
         + abs(list[1][1] - list[-1][1]) ^ 2)
        , 0.5)
    if c == 0:
        c = 0.1
    if b == 0:
        b = 0.1
    val = round((round(a, 8) ** 2 - round(b, 8) ** 2 - round(c, 8) ** 2) / (-2 * round(b, 8) * round(c, 8)), 6)
    # print(val)
    if val < -1:
        # print(round(val-math.trunc(val),8))
        val = round(val - math.trunc(val), 8)
    else:
        val = (math.acos(val) * 180) / math.pi
    if val < 0:
        val = 180 + val
    print("point1: ", a, " point2: ", b, " point3: ", c, " angle :", val)
    ang[1].append(val)
    ang[0].append([list[1], list[0], list[-1]])
    return ang


# To convert RGB image to Gray
gray = RGB2GRAY(img)
thresh = threshold(gray, 0.38 * 255)
canny = edgeDetection(thresh)
point_list = []
eps = 80

getCoordinatesY(canny)
getCoordinatesX(canny)
coordinates = coordinatesX + coordinatesY

rdp1 = RDP(coordinatesX, coordinatesY, eps)
# Angle values [[[point1],[point2],[point3]],[angle value]]---> 2D array first points second angle values
angle(rdp1)
arc = 0
# To plot the RDP result
result1 = RDP_Result(rdp1, thresh, arc)

"""f = plt.figure()
f.add_subplot(2, 2, 1)
plt.imshow(gray)
f.add_subplot(2, 2, 2)
plt.imshow(thresh)
f.add_subplot(2, 2, 3)
plt.imshow(canny)
f.add_subplot(2, 2, 4)
plt.imshow(result1)"""
plt.imshow(result1)
plt.show(block=True)
plt.show()
