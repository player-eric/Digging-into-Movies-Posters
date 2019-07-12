import cv2 as cv
import os
from PIL import Image
import numpy as np
import pandas as pd
import csv
from math import sqrt
import sys
import os
import numpy as np
import glob


# 计算两个海报间距离
def distance(lst1, lst2):
    sum = 0
    for i in range(len(lst1)):
      d = lst1[i]-lst2[i]
      sum += d*d
    sum = sqrt(sum)
    return round(sum, 2)


# 分割海报并保存在同一文件夹
def crop(filepath):
    # 记录海报对应电影名，用于新建文件夹
    imnames = []
    for parent, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            imnames.append(os.path.splitext(filename)[0])
    # 图片导入List
    images = []
    for f in glob.iglob(filepath + '\\*.jpg'):
        im = Image.open(f)
        images.append(im)

    t = 0
    for image in images:
        print(filepath + '\\' + imnames[t])
        # 新建文件夹
        os.mkdir(filepath + '\\' + imnames[t])
        # 分割图片
        for i in range(66):
            for j in range(25):
                box = (7 * j, 4 * i, 7 * (j + 1), 4 * (i + 1))
                region = image.crop(box)
                region.save(filepath + '\\' + imnames[t] + '\\' + imnames[t] + str(i) + str(j) + ".jpg")
        t += 1


# 获取单个分割图像RGB
def get_rgb(filepath):
    im = Image.open(filepath)
    width = im.size[0]
    height = im.size[1]
    im = im.convert('RGB')
    array = []
    # 逐像素获取
    for x in range(width):
        for y in range(height):
            r, g, b = im.getpixel((x, y))
            rgb = (r, g, b)
            array += [[i for i in rgb]]
    # 求平均值
    red = np.mean([n[0] for n in array])
    green = np.mean([n[1] for n in array])
    blue = np.mean([n[2] for n in array])
    return [round(i, 2) for i in [red, green, blue]]


# 计算每个海报RGB
def poster_rgb(filepath):
    rgb = []
    # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            img_path = os.path.join(parent, filename)
            rgb += get_rgb(img_path)
    # print(rgb)
    print(parent + 'DONE')
    return rgb


# 存储sim.txt和labels.txt
def text_save(filename, data, flag):
    file = open(filename,'a')
    for i in range(len(data)):
        # 去除[],这两行按数据不同，可以选择
        s = str(data[i]).replace('[', '').replace(']', '')
        # 去除单引号，逗号，每行末尾追加换行符
        s = s.replace("'", '').replace(',', '').replace('\n', '') + '\n'
        if flag:
            s = s.replace(' ', '')
        file.write(s)
    file.close()
    print("保存文件成功")


if __name__ == '__main__':
    rgb = {}
    labels = []
    num = 0
    filepath = 'C:\\Users\\X1 Yoga\\Desktop\\NUS\\CD\\Data Set\\试验\\source'
    # 下面两行打开csv文件
    # csvfile = open(filepath + '.csv', "w")
    # writer = csv.writer(csvfile)
    ###########################################
    # 下面一行代码只在还未分割图片时使用，若已
    # 经分割过，就可注释掉
    crop(filepath)
    ###########################################
    for parent, dirnames, filenames in os.walk(filepath):
        for dirname in dirnames:  # 输出文件夹信息
            num += 1
            labels.append(dirname)
            rgb[dirname] = poster_rgb(parent + '\\' + dirname)
            # writer.writerow([dirname] + poster_rgb(parent + '\\' + dirname))
    dismat = np.zeros((num, num))
    # print(labels)
    # 生成相似度矩阵
    for x in labels:
        for y in labels:
            if x == y:
                continue
            dist = distance(rgb[x], rgb[y])
            # print(dist)
            dismat[labels.index(x)][labels.index(y)] = dist
            dismat[labels.index(y)][labels.index(x)] = dist
    print(dismat)
    text_save(filepath + '\\sim.txt', dismat, 0)
    text_save(filepath + '\\labels.txt', labels, 1)
    # print(rgb['the wild bunch'])
    # dataframe = pd.DataFrame(rgb)
    # dataframe.to_csv(parent + '.csv', float_format='%.2f', index=False)
