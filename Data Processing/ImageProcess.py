import numpy as np
import cv2 as cv
import os
import time
import shutil
import zipfile


def img_resize(filepath):
    num = 0
    for parent, dirnames, filenames in os.walk(filepath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 输出文件信息
            num += 1
            img_path = os.path.join(parent, filename)  # 输出文件路径信息
            # print(img_path)
            img = cv.imread(img_path)  # 读取图片
            res = cv.resize(img, (92, 112), interpolation=cv.INTER_AREA)  #改变图片尺寸
            cv.imwrite(img_path, res)  #原路径存放
    return(num)


def img_store(filepath, dstpath, num, labels):
    for parent, dirnames, filenames in os.walk(filepath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        i = 0
        for filename in filenames:  # 输出文件信息
            n = 1
            img_path = os.path.join(parent, filename)  # 输出文件路径信息
            # print(img_path)
            os.mkdir(os.path.join(dstpath, labels[i]))
            src = os.path.join(os.path.abspath(parent), filename)  # 重命名
            while n <= num:
                dst = os.path.join(os.path.abspath(os.path.join(dstpath, labels[i])), str(n) + '.jpg')  # 执行操作
                shutil.copyfile(src, dst)
                n += 1
            i += 1


def file_zip(path, pt):
    zipName = path + 'data' + pt + '.zip'

    f = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(path + 'data' + pt):
        fpath = dirpath.replace(path + 'data' + pt, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            # print(filename)
            f.write(os.path.join(dirpath, filename), 'data\\' + fpath + filename)
    f.close()


if __name__ == '__main__':
    path = 'C:\\Users\\X1 Yoga\\Desktop\\NUS\\CD\\Data Set\\data_sample\\'
    num = img_resize(path + 'datasource')
    labels = ['s' + str(i) for i in range(num)]
    # labels = ['s1', 's8', 's10', 's11', 's14', 's18', 's21', 's25', 's26', 's27',
    #           's28', 's29', 's30', 's31', 's34', 's37', 's40', 's41']
    # print(len(labels))
    pt = time.strftime("%d%H%M%S", time.localtime())
    os.mkdir(path + 'data' + pt)
    img_store(path + 'datasource', path + 'data' + pt, 1, labels)
    # dst = path + 'data' + pt + '.zip'
    # src = path + 'data' + pt
    # os.system("zip -r dst src")
    file_zip(path, pt)
    shutil.rmtree(path + 'data' + pt)

