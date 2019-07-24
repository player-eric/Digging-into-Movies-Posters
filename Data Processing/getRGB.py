import cv2 as cv
from PIL import Image
import numpy as np
import pandas as pd
from math import sqrt
import sys
import os
import numpy as np
import glob
import shutil


def make_regalur_image(img, size=(182, 268)):
    return img.resize(size).convert('RGB')


def split_image(img, part_size=(13, 67)):
    w, h = img.size
    pw, ph = part_size

    assert w % pw == h % ph == 0

    return [img.crop((i, j, i + pw, j + ph)).copy() \
            for i in range(0, w, pw) \
            for j in range(0, h, ph)]


def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)


def calc_similar(li, ri):
    # return hist_similar(li.histogram(), ri.histogram())
    return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0


def calc_similar_by_path(lf, rf):
    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
    return calc_similar(li, ri)


def make_doc_data(lf, rf):
    li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
    li.save(lf + '_regalur.png')
    ri.save(rf + '_regalur.png')
    fd = open('stat.csv', 'w')
    fd.write('\n'.join(l + ',' + r for l, r in zip(map(str, li.histogram()), map(str, ri.histogram()))))
    # print >>fd, '\n'
    # fd.write(','.join(map(str, ri.histogram())))
    fd.close()
    from PIL import ImageDraw
    li = li.convert('RGB')
    draw = ImageDraw.Draw(li)
    for i in range(0, 256, 64):
        draw.line((0, i, 256, i), fill='#ff0000')
        draw.line((i, 0, i, 256), fill='#ff0000')
    li.save(lf + '_lines.png')


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
    if os.path.exists(filepath + '\\sim_labels'):
        shutil.rmtree(filepath + '\\sim_labels')
    if os.path.exists(filepath + '\\sim.txt'):
        os.remove(filepath + '\\sim.txt')
    if os.path.exists(filepath + '\\labels.txt'):
        os.remove(filepath + '\\labels.txt')

    # for parent, dirnames, filenames in os.walk(filepath):
    #     for filename in filenames:
    #         os.rename(parent + '/' + filename, parent + '/' + filename.replace(' ', ''))
    # 下面两行打开csv文件
    # csvfile = open(filepath + '.csv', "w")
    # writer = csv.writer(csvfile)
    ###########################################
    # 下面一行代码只在还未分割图片时使用，若已
    # 经分割过，就可注释掉
    # crop(filepath)
    ###########################################

    for parent, dirnames, filenames in os.walk(filepath):
        for filname in filenames:  # 输出文件夹信息
            num += 1
            # labels.append(dirname)
            # rgb[dirname] = poster_rgb(parent + '\\' + dirname)
            # writer.writerow([dirname] + poster_rgb(parent + '\\' + dirname))
    dismat = np.zeros((num, num))
    num = 0
    for parent, dirnames, filenames in os.walk(filepath):
        for filename1 in filenames:  # 输出文件夹信息
            # if os.path.splitext(filename1)[1] == 'jpg':
                m = 0
                labels.append(os.path.splitext(filename1)[0])
                for filename2 in filenames:
                    dist = calc_similar_by_path(parent + '\\' + filename1, parent + '\\' + filename2)
                    if dist > 1:
                        dismat[num][m] = 0
                    else:
                        dismat[num][m] = 1 - dist
                    print(filename1 + 'and' + filename2 + 'DONE!')
                    m += 1
                    # rgb[dirname] = poster_rgb(parent + '\\' + dirname)
                num += 1

    # print(labels)
    # 生成相似度矩阵
    # for x in labels:
    #     for y in labels:
    #         if x == y:
    #             continue
    #         dist = distance(rgb[x], rgb[y])
    #         # print(dist)
    #         dismat[labels.index(x)][labels.index(y)] = dist
    #         dismat[labels.index(y)][labels.index(x)] = dist
    print(dismat)
    os.mkdir(filepath + '\\sim_labels')
    text_save(filepath + '\\sim_labels' + '\\sim.txt', dismat, 0)
    text_save(filepath + '\\sim_labels' + '\\labels.txt', labels, 1)

    # print(rgb['the wild bunch'])
    # dataframe = pd.DataFrame(rgb)
    # dataframe.to_csv(parent + '.csv', float_format='%.2f', index=False)
